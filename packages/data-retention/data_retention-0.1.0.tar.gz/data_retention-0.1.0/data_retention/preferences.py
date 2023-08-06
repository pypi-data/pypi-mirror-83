from papermerge.core.preferences import Section
from dynamic_preferences.types import IntegerPreference
from dynamic_preferences.users.registries import user_preferences_registry


@user_preferences_registry.register
class DummyOption(IntegerPreference):
    help_text = """
    Dummy
"""
    section = Section(
        "data_retention",
        verbose_name="Data Retention",
        help_text="""
How long should a document be stored? When should a document be destroyed?
""",
        icon_name="balance-scale"
    )
    name = 'page_count'
    default = 15
