from enum import Enum


class SubscribedFields(Enum):
    MESSAGES = "messages"
    MESSAGING_POSTBACKS = "messaging_postbacks"
    MESSAGING_OPTINS = "messaging_optins"
    MESSAGE_DELIVERIES = "message_deliveries"
    MESSAGE_READS = "message_reads"
    MESSAGING_PAYMENTS = "messaging_payments"
    MESSAGING_PRE_CHECKOUTS = "messaging_pre_checkouts"
    MESSAGING_CHECKOUT_UPDATES = "messaging_checkout_updates"
    MESSAGING_ACCOUNT_LINKING = "messaging_account_linking"
    MESSAGING_REFERRALS = "messaging_referrals"
    MESSAGE_ECHOES = "message_echoes"
    MESSAGING_GAME_PLAYS = "messaging_game_plays"
    STANDBY = "standby"
    MESSAGING_HANDOVERS = "messaging_handovers"
    MESSAGING_POLICY_ENFORCEMENT = "messaging_policy_enforcement"
    MESSAGE_REACTIONS = "message_reactions"
    INBOX_LABELS = "inbox_labels"
