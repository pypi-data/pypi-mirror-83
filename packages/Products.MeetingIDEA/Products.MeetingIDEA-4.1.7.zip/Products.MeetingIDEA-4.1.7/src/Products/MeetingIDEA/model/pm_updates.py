from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.config import WriteRiskyConfig

from Products.Archetypes.atapi import BooleanField, Schema, TextField, ReferenceField, RichWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget


def update_item_schema(baseSchema):
    specificSchema = Schema((

        TextField(
            name='internalCommunication',
            widget=RichWidget(
                condition="python: here.portal_plonemeeting.isManager(here)",
                description="InternalCommunication",
                description_msgid="item_internalCommunication_descr",
                label='InternalCommunication',
                label_msgid='PloneMeeting_label_internalCommunication',
                i18n_domain='PloneMeeting',
            ),
            optional=True,
            default_content_type="text/html",
            allowable_content_types=('text/html',),
            default_output_type="text/x-html-safe",
        ),

        ReferenceField(
            name='strategicAxis',
            keepReferencesOnCopy=True,
            widget=ReferenceBrowserWidget(
                description="StrategicAxis",
                description_msgid="item_strategicAxis_descr",
                condition="python: here.attributeIsUsed('strategicAxis')",
                allow_search=True,
                allow_browse=False,
                startup_directory_method="classifierStartupDirectory",
                force_close_on_insert=False,
                restrict_browsing_to_startup_directory=True,
                base_query="classifierBaseQuery",
                show_results_without_query=True,
                label='StrategicAxis',
                label_msgid='PloneMeeting_label_strategicAxis',
                i18n_domain='PloneMeeting',
            ),
            multiValued=True,
            relationship="ItemStrategicAxis",
            allowed_types=('MeetingCategory',),
            optional=True,
        ),)
    )

    baseSchema['detailedDescription'].widget.description = "DetailedDescriptionMethode"
    baseSchema['detailedDescription'].widget.description_msgid = "detailedDescription_item_descr"
    completeItemSchema = baseSchema + specificSchema.copy()
    completeItemSchema.moveField('strategicAxis', after='detailedDescription')
    return completeItemSchema


MeetingItem.schema = update_item_schema(MeetingItem.schema)


def update_meeting_schema(baseSchema):
    specificSchema = Schema((
    ), )

    baseSchema['assembly'].widget.description_msgid = "assembly_meeting_descr"

    completeMeetingSchema = baseSchema + specificSchema.copy()
    return completeMeetingSchema


Meeting.schema = update_meeting_schema(Meeting.schema)


def update_config_schema(baseSchema):
    specificSchema = Schema((
        BooleanField(
            name='initItemDecisionIfEmptyOnDecide',
            default=True,
            widget=BooleanField._properties['widget'](
                description="InitItemDecisionIfEmptyOnDecide",
                description_msgid="init_item_decision_if_empty_on_decide",
                label='Inititemdecisionifemptyondecide',
                label_msgid='MeetingIDEA_label_initItemDecisionIfEmptyOnDecide',
                i18n_domain='PloneMeeting'),
            write_permission=WriteRiskyConfig,
        ),
    ), )

    completeConfigSchema = baseSchema + specificSchema.copy()
    return completeConfigSchema


MeetingConfig.schema = update_config_schema(MeetingConfig.schema)

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses

registerClasses()
