###
##  Django Proxypay Reference Model
#

# django stuff
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from dateutil import parser

# proxypay stuff
from proxypay.api import api
from proxypay.exceptions import ProxypayException
from proxypay.signals import reference_paid, reference_created

# ==========================================================================================================

###
## Paymentt Status
#

PAYMENT_STATUS_PAID = 'paid'
PAYMENT_STATUS_WAIT = 'wait'

# ==========================================================================================================

"""Proxypay References Model Manager"""

class ReferenceModelManager(models.Manager):

    def create(self, **kwargs):
        # creating the signal
        reference = super(ReferenceModelManager, self).create(**kwargs)
        # Dispatching Signal
        reference_created.send(
            reference.__class__, 
            reference=reference
        )
        #
        return reference

"""Proxypay References Model"""

class Reference(models.Model):

    ###
    ## Model Attributes
    #

    # reference id
    reference           = models.IntegerField(verbose_name=_('Reference'), unique=True, editable=False)
    amount              = models.DecimalField(verbose_name=_('Amount'), max_digits=12, decimal_places=2, editable=False)
    entity              = models.CharField(verbose_name=_('Entity'), max_length=100, null=True, default=None, editable=False)
    fields              = models.JSONField(default=dict)
    # reference payment status: canceled, paid, expired, wait
    payment_status      = models.CharField(max_length=10, default=PAYMENT_STATUS_WAIT, editable=False)
    payment             = models.JSONField(default=None, null=True)

    is_paid    = models.BooleanField(default=False)
    paid_at    = models.DateTimeField(default=None, null=True)
    # date
    expires_in = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Update At'), auto_now=True)


    ###
    ##  Manager
    #

    objects = ReferenceModelManager()

    ###
    ##  Methods
    #

    # cancel reference on proxypay and delete instance

    def delete(self):

        """Delete payment reference from Proxypay and Database"""

        # deleting from proxypay
        deleted = api.delete_reference(self.reference)
        # 
        if deleted:
            return super(Reference, self).delete()

        raise ProxypayException('Error when trying to delete the reference in the Proxypay')

    # update reference payment status to paid

    def paid(self, payment_data):

        """
        Update reference payment status to paid
        Suitable for use with Proxypay's Webhook
        """

        if not self.payment:
            
            # passando os dados de pagamento na instancia
            self.payment        = payment_data
            self.payment_status = PAYMENT_STATUS_PAID
            self.is_paid        = True

            try:
                self.paid_at = parser.isoparse(self.payment.get('datetime'))
            except:
                self.paid_at = now()
                
            self.save()

            #
            self.__dispatch_paid_signal()

    # Check if a reference was paid

    def check_payment(self):

        """
        Checks whether the referral payment has already been processed.
        Initially check on the instanse, if it is not processed, check the Proxypay API to be sure. 
        Returns payment data or false
        """

        if not self.payment:
            # check from api
            payment = api.check_reference_payment(self.reference)
            # case already paid
            if payment:
                self.paid(payment)
            # returns payment data or false
            return payment
        # returning the payment data already registered
        return self.payment

    ###
    ## Property Methods
    #

    # expired status

    @property
    def expired(self):
        if self.expires_in:
            return self.expires_in < now()
        return False

    ###
    ## Classe Method
    #

    def __str__(self):
        return f"Proxypay Reference: {self.reference}"

    def __repr__(self):
        return f"Proxypay Reference: {self.reference}"

    ###
    ## Some Utils
    #

    def __dispatch_paid_signal(self):
        # Dispatching Signal
        reference_paid.send(
            self.__class__, 
            reference=self
        )
        