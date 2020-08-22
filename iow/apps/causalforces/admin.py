from django.contrib import admin

from .models import Current_Reality, InstructionVideos, FirstLevelContent, SecondLevelContent, ThirdLevelContent, \
     Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('A Negative I Want in My Life', {
            'fields': ['negative_i_want_section_1_button_text', 'negative_i_want_section_1_show_less_text',
                       'negative_i_want_s1_l1_first_field_title', 'negative_i_want_s1_l1_second_field_title',
                       'negative_i_want_s1_l1_third_field_title', 'negative_i_want_s1_l2_f1_header_title',
                       'negative_i_want_s1_l2_f2_header_title', 'negative_i_want_s1_l2_f3_header_title',
                       'negative_i_want_s1_l3_f1_title', 'negative_i_want_s1_l3_f2_title',
                       'negative_i_want_s1_l3_f3_title', 'negative_i_want_section_2_button_text',
                       'negative_i_want_section_2_show_less_text', 'negative_i_want_s2_l2_first_field_title',
                       'negative_i_want_s2_l2_second_field_title', 'negative_i_want_s2_l2_third_field_title',
                       'negative_i_want_s2_l2_f1_header_title', 'negative_i_want_s2_l2_f2_header_title', 
                       'negative_i_want_s2_l2_f3_header_title', 'negative_i_want_s2_l3_f1_title',
                       'negative_i_want_s2_l3_f2_title', 'negative_i_want_s2_l3_f3_title']}),
        ('Steps to Turn Negative', {
            'fields': ['steps_to_turn_negative_section_1_button_text',
                       'steps_to_turn_negative_section_1_show_less_text',
                       'steps_to_turn_negative_s1_l1_first_field_title',
                       'steps_to_turn_negative_s1_l1_second_field_title',
                       'steps_to_turn_negative_s1_l1_third_field_title', 'steps_to_turn_negative_s1_l2_f1_header_title',
                       'steps_to_turn_negative_s1_l2_f2_header_title', 'steps_to_turn_negative_s1_l2_f3_header_title',
                       'steps_to_turn_negative_s1_l3_button1_text', 'steps_to_turn_negative_s1_l3_button2_text',
                       'steps_to_turn_negative_s1_l3_button3_text', 'steps_to_turn_negative_s1_l3_f1_title',
                       'steps_to_turn_negative_s1_l3_f2_title', 'steps_to_turn_negative_s1_l3_f3_title',
                       'steps_to_turn_negative_section_2_button_text',
                       'steps_to_turn_negative_section_2_show_less_text',
                       'steps_to_turn_negative_s2_l2_first_field_title',
                       'steps_to_turn_negative_s2_l2_second_field_title',
                       'steps_to_turn_negative_s2_l2_third_field_title', 'steps_to_turn_negative_s2_l2_f1_header_title',
                       'steps_to_turn_negative_s2_l2_f2_header_title', 'steps_to_turn_negative_s2_l2_f3_header_title',
                       'steps_to_turn_negative_s2_l3_button1_text', 'steps_to_turn_negative_s2_l3_button2_text',
                       'steps_to_turn_negative_s2_l3_button3_text', 'steps_to_turn_negative_s2_l3_f1_title',
                       'steps_to_turn_negative_s2_l3_f2_title', 'steps_to_turn_negative_s2_l3_f3_title']}),
        ('Weak & Disgrace', {
            'fields': ['weak_and_disgrace_section_1_button_text', 'weak_and_disgrace_section_1_show_less_text',
                       'weak_and_disgrace_s1_l1_first_field_title', 'weak_and_disgrace_s1_l1_second_field_title',
                       'weak_and_disgrace_s1_l1_third_field_title', 'weak_and_disgrace_s1_l2_f1_header_title',
                       'weak_and_disgrace_s1_l2_f2_header_title', 'weak_and_disgrace_s1_l2_f3_header_title',
                       'weak_and_disgrace_s1_l3_button1_text', 'weak_and_disgrace_s1_l3_button2_text',
                       'weak_and_disgrace_s1_l3_button3_text', 'weak_and_disgrace_s1_l3_f1_title',
                       'weak_and_disgrace_s1_l3_f2_title', 'weak_and_disgrace_s1_l3_f3_title',
                       'weak_and_disgrace_section_2_button_text', 'weak_and_disgrace_section_2_show_less_text',
                       'weak_and_disgrace_s2_l2_first_field_title', 'weak_and_disgrace_s2_l2_second_field_title',
                       'weak_and_disgrace_s2_l2_third_field_title', 'weak_and_disgrace_s2_l2_f1_header_title',
                       'weak_and_disgrace_s2_l2_f2_header_title', 'weak_and_disgrace_s2_l2_f3_header_title',
                       'weak_and_disgrace_s2_l3_button1_text', 'weak_and_disgrace_s2_l3_button2_text',
                       'weak_and_disgrace_s2_l3_button3_text', 'weak_and_disgrace_s2_l3_f1_title',
                       'weak_and_disgrace_s2_l3_f2_title', 'weak_and_disgrace_s2_l3_f3_title']}),
        ('Low Performance Ability', {
            'fields': ['low_performance_ability_section_1_button_text',
                       'low_performance_ability_section_1_show_less_text',
                       'low_performance_ability_s1_l1_first_field_title',
                       'low_performance_ability_s1_l1_second_field_title',
                       'low_performance_ability_s1_l1_third_field_title',
                       'low_performance_ability_s1_l2_f1_header_title',
                       'low_performance_ability_s1_l2_f2_header_title',
                       'low_performance_ability_s1_l2_f3_header_title',
                       'low_performance_ability_s1_l3_button1_text', 'low_performance_ability_s1_l3_button2_text',
                       'low_performance_ability_s1_l3_button3_text', 'low_performance_ability_s1_l3_f1_title',
                       'low_performance_ability_s1_l3_f2_title', 'low_performance_ability_s1_l3_f3_title',
                       'low_performance_ability_section_2_button_text',
                       'low_performance_ability_section_2_show_less_text',
                       'low_performance_ability_s2_l2_first_field_title',
                       'low_performance_ability_s2_l2_second_field_title',
                       'low_performance_ability_s2_l2_third_field_title',
                       'low_performance_ability_s2_l2_f1_header_title',
                       'low_performance_ability_s2_l2_f2_header_title',
                       'low_performance_ability_s2_l2_f3_header_title',
                       'low_performance_ability_s2_l3_button1_text', 'low_performance_ability_s2_l3_button2_text',
                       'low_performance_ability_s2_l3_button3_text', 'low_performance_ability_s2_l3_f1_title',
                       'low_performance_ability_s2_l3_f2_title', 'low_performance_ability_s2_l3_f3_title']}),
        ('Current Habits of Ability', {
            'fields': ['current_habits_of_ability_section_1_button_text',
                       'current_habits_of_ability_section_1_show_less_text',
                       'current_habits_of_ability_s1_l1_first_field_title',
                       'current_habits_of_ability_s1_l1_second_field_title',
                       'current_habits_of_ability_s1_l1_third_field_title',
                       'current_habits_of_ability_s1_l2_f1_header_title',
                       'current_habits_of_ability_s1_l2_f2_header_title',
                       'current_habits_of_ability_s1_l2_f3_header_title',
                       'current_habits_of_ability_s1_l3_button1_text', 'current_habits_of_ability_s1_l3_button2_text',
                       'current_habits_of_ability_s1_l3_button3_text', 'current_habits_of_ability_s1_l3_f1_title',
                       'current_habits_of_ability_s1_l3_f2_title', 'current_habits_of_ability_s1_l3_f3_title',
                       'current_habits_of_ability_section_2_button_text',
                       'current_habits_of_ability_section_2_show_less_text',
                       'current_habits_of_ability_s2_l2_first_field_title',
                       'current_habits_of_ability_s2_l2_second_field_title',
                       'current_habits_of_ability_s2_l2_third_field_title',
                       'current_habits_of_ability_s2_l2_f1_header_title',
                       'current_habits_of_ability_s2_l2_f2_header_title',
                       'current_habits_of_ability_s2_l2_f3_header_title',
                       'current_habits_of_ability_s2_l3_button1_text', 'current_habits_of_ability_s2_l3_button2_text',
                       'current_habits_of_ability_s2_l3_button3_text', 'current_habits_of_ability_s2_l3_f1_title',
                       'current_habits_of_ability_s2_l3_f2_title', 'current_habits_of_ability_s2_l3_f3_title']}),
        ('Habit-ats Outside of Me', {
            'fields': ['habitats_outside_of_me_section_1_button_text',
                       'habitats_outside_of_me_section_1_show_less_text',
                       'habitats_outside_of_me_s1_l1_first_field_title',
                       'habitats_outside_of_me_s1_l1_second_field_title',
                       'habitats_outside_of_me_s1_l1_third_field_title', 'habitats_outside_of_me_s1_l2_f1_header_title',
                       'habitats_outside_of_me_s1_l2_f2_header_title', 'habitats_outside_of_me_s1_l2_f3_header_title',
                       'habitats_outside_of_me_s1_l3_button1_text', 'habitats_outside_of_me_s1_l3_button2_text',
                       'habitats_outside_of_me_s1_l3_button3_text', 'habitats_outside_of_me_s1_l3_f1_title',
                       'habitats_outside_of_me_s1_l3_f2_title', 'habitats_outside_of_me_s1_l3_f3_title',
                       'habitats_outside_of_me_section_2_button_text',
                       'habitats_outside_of_me_section_2_show_less_text',
                       'habitats_outside_of_me_s2_l2_first_field_title',
                       'habitats_outside_of_me_s2_l2_second_field_title',
                       'habitats_outside_of_me_s2_l2_third_field_title', 'habitats_outside_of_me_s2_l2_f1_header_title',
                       'habitats_outside_of_me_s2_l2_f2_header_title', 'habitats_outside_of_me_s2_l2_f3_header_title',
                       'habitats_outside_of_me_s2_l3_button1_text', 'habitats_outside_of_me_s2_l3_button2_text',
                       'habitats_outside_of_me_s2_l3_button3_text', 'habitats_outside_of_me_s2_l3_f1_title',
                       'habitats_outside_of_me_s2_l3_f2_title', 'habitats_outside_of_me_s2_l3_f3_title']}),
    ]

    def has_add_permission(self, request):
        return not Settings.objects.exists()


@admin.register(FirstLevelContent)
class FirstLevelContentAdmin(admin.ModelAdmin):
    list_filter = ('show_less_content',)
    list_display = (
        'show_less_content',
    )


@admin.register(SecondLevelContent)
class SecondLevelContentAdmin(admin.ModelAdmin):
    list_filter = ('first_level',)
    list_display = (
        'id', 'first_level',
    )
    list_display_links = (
        'id', 'first_level',
    )
    fieldsets = [('First Level', {
        'fields': ['first_level']}),
                 ('First Fields Show More Content', {
                     'fields': ['first_f1_show_more_text', 'second_f1_show_more_text', 'third_f1_show_more_text']}),
                 ('Second Field Show More Content', {
                     'fields': ['first_f2_show_more_text', 'second_f2_show_more_text', 'third_f2_show_more_text']}),
                 ('Third Field Show More Content', {
                     'fields': ['first_f3_show_more_text', 'second_f3_show_more_text', 'third_f3_show_more_text']}),
                 ]


@admin.register(ThirdLevelContent)
class ThirdLevelContentAdmin(admin.ModelAdmin):
    list_filter = ('second_level',)
    list_display = (
        'id', 'second_level',
    )
    list_display_links = (
        'id', 'second_level',
    )
    fieldsets = [('Second Level', {
        'fields': ['second_level']}),
                 ('1st Heading 1st Fields Set', {
                     'fields': ['f1_1st_f1_text', 'f1_1st_f2_text', 'f1_1st_f3_text']}),
                 ('1st Heading 2nd Fields Set', {
                     'fields': ['f1_2nd_f1_text', 'f1_2nd_f2_text', 'f1_2nd_f3_text']}),
                 ('1st Heading 3rd Fields Set', {
                     'fields': ['f1_3rd_f1_text', 'f1_3rd_f2_text', 'f1_3rd_f3_text']}),
                 ('2nd Heading 1st Fields Set', {
                     'fields': ['f2_1st_f1_text', 'f2_1st_f2_text', 'f2_1st_f3_text']}),
                 ('2nd Heading 2nd Fields Set', {
                     'fields': ['f2_2nd_f1_text', 'f2_2nd_f2_text', 'f2_2nd_f3_text']}),
                 ('2nd Heading 3rd Fields Set', {
                     'fields': ['f2_3rd_f1_text', 'f2_3rd_f2_text', 'f2_3rd_f3_text']}),
                 ('3rd Heading 1st Fields Set', {
                     'fields': ['f3_1st_f1_text', 'f3_1st_f2_text', 'f3_1st_f3_text']}),
                 ('3rd Heading 2nd Fields Set', {
                     'fields': ['f3_2nd_f1_text', 'f3_2nd_f2_text', 'f3_2nd_f3_text']}),
                 ('3rd Heading 3rd Fields Set', {
                     'fields': ['f3_3rd_f1_text', 'f3_3rd_f2_text', 'f3_3rd_f3_text']}),
                 ]

@admin.register(Current_Reality)
class WantAdmin(admin.ModelAdmin):
    list_filter = ('category', 'subcategory')
    list_display = (
        'name', 'category', 'subcategory'
    )
    ordering = ('order',)

    fieldsets = [
        (None, {'fields': ['name', 'category', 'subcategory', 'order','related_want']}),
        ('A Negative I Want in My Life', {
            'fields': ['negative_i_want_show_more_content_1', 'negative_i_want_show_more_content_2']}),
        ('Steps to Turn negative', {
            'fields': ['steps_to_turn_negative_show_more_content_1', 'steps_to_turn_negative_show_more_content_2']}),
        ('Power & Grace', {
            'fields': ['weak_and_disgrace_show_more_content_1', 'weak_and_disgrace_show_more_content_2']}),
        ('Low Performance Ability', {
            'fields': ['low_performance_ability_show_more_content_1',
                       'low_performance_ability_show_more_content_2']}),
        ('Current Habits of Ability', {
            'fields': ['current_habits_of_ability_show_more_content_1',
                       'current_habits_of_ability_show_more_content_2']}),
        ('Habit-ats Outside of Me', {
            'fields': ['habitats_outside_of_me_show_more_content_1', 'habitats_outside_of_me_show_more_content_2']}),
    ]


@admin.register(InstructionVideos)
class InstructionVideosAdmin(admin.ModelAdmin):
    list_display = (
        'current_reality_instruction_video', 'steps_instruction_video', 'weak_instruction_video',
        'ability_instruction_video', 'current_habits_instruction_video', 'habitats_instruction_video'
    )
    list_display_links = (
        'current_reality_instruction_video', 'steps_instruction_video', 'weak_instruction_video', 'ability_instruction_video',
        'current_habits_instruction_video', 'habitats_instruction_video')

    def has_add_permission(self, request):
        return not InstructionVideos.objects.exists()
