from django.db import models

class MessageManager(models.Manager):
    """ Manager for the :class:`Message` model. """

    def get_mailbox_for(self, user, mailbox='inbox'):
        """
        Returns all messages in the mailbox that were received by the given
        user and are not marked as deleted.

        :param user:
            The :class:`User` for who the mailbox is for.

        :param mailbox:
            String containing the mailbox which is requested. This can be
            either ``inbox``, ``outbox``, ``drafts`` or ``trash``.

        :return:
            Queryset containing :class:`Messages` or ``ValueError`` if the
            invalid mailbox is supplied.

        """
        if mailbox == 'outbox':
            messages = self.filter(sender=user,
                                   sender_deleted_at__isnull=True,
                                   sent_at__isnull=False)

        elif mailbox == 'drafts':
            messages = self.filter(sender=user,
                                   sent_at__isnull=True,
                                   sender_deleted_at__isnull=True)

        elif mailbox == 'trash':
            received = self.filter(recipients=user,
                                   messagerecipient__deleted_at__isnull=False)

            sent = self.filter(sender=user,
                               sender_deleted_at__isnull=False)

            messages = received | sent

        elif mailbox == 'inbox':
            messages = self.filter(recipients=user,
                                   messagerecipient__deleted_at__isnull=True)

        else:
            raise ValueError("mailbox must be either inbox, outbox, drafts or trash")

        return messages

    def get_inbox_for(self, user):
        """ Wrapper for :func:`get_mailbox_for` to get the users inbox. """
        return self.get_mailbox_for(user, 'inbox')

    def get_outbox_for(self, user):
        """ Wrapper for :func:`get_mailbox_for` to get the users outbox. """
        return self.get_mailbox_for(user, 'outbox')

    def get_drafts_for(self, user):
        """ Wrapper for :func:`get_mailbox_for` to get the users drafts. """
        return self.get_mailbox_for(user, 'drafts')

    def get_trash_for(self, user):
        """ Wrapper for :func:`get_mailbox_for` to get the users trash. """
        return self.get_mailbox_for(user, 'trash')