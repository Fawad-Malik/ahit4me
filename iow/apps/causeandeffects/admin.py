from django.contrib import admin

from .models import Want, InstructionVideos, FirstLevelContent, SecondLevelContent, ThirdLevelContent, \
     Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('A Positive I Want in My Life', {
            'fields': ['positive_i_want_section_1_button_text', 'positive_i_want_section_1_show_less_text',
                       'positive_i_want_s1_l1_first_field_title', 'positive_i_want_s1_l1_second_field_title',
                       'positive_i_want_s1_l1_third_field_title', 'positive_i_want_s1_l2_f1_header_title',
                       'positive_i_want_s1_l2_f2_header_title', 'positive_i_want_s1_l2_f3_header_title',
                       'positive_i_want_s1_l3_f1_title', 'positive_i_want_s1_l3_f2_title',
                       'positive_i_want_s1_l3_f3_title', 'positive_i_want_section_2_button_text',
                       'positive_i_want_section_2_show_less_text', 'positive_i_want_s2_l2_first_field_title', 
                       'positive_i_want_s2_l2_second_field_title', 'positive_i_want_s2_l2_third_field_title', 
                       'positive_i_want_s2_l2_f1_header_title', 'positive_i_want_s2_l2_f2_header_title',
                       'positive_i_want_s2_l2_f3_header_title', 'positive_i_want_s2_l3_f1_title',
                       'positive_i_want_s2_l3_f2_title', 'positive_i_want_s2_l3_f3_title']}),
        ('Steps to Turn Positive', {
            'fields': ['steps_to_turn_positive_section_1_button_text',
                       'steps_to_turn_positive_section_1_show_less_text',
                       'steps_to_turn_positive_s1_l1_first_field_title',
                       'steps_to_turn_positive_s1_l1_second_field_title',
                       'steps_to_turn_positive_s1_l1_third_field_title', 'steps_to_turn_positive_s1_l2_f1_header_title',
                       'steps_to_turn_positive_s1_l2_f2_header_title', 'steps_to_turn_positive_s1_l2_f3_header_title',
                       'steps_to_turn_positive_s1_l3_button1_text', 'steps_to_turn_positive_s1_l3_button2_text',
                       'steps_to_turn_positive_s1_l3_button3_text', 'steps_to_turn_positive_s1_l3_f1_title',
                       'steps_to_turn_positive_s1_l3_f2_title', 'steps_to_turn_positive_s1_l3_f3_title',
                       'steps_to_turn_positive_section_2_button_text',
                       'steps_to_turn_positive_section_2_show_less_text',
                       'steps_to_turn_positive_s2_l2_first_field_title',
                       'steps_to_turn_positive_s2_l2_second_field_title',
                       'steps_to_turn_positive_s2_l2_third_field_title', 'steps_to_turn_positive_s2_l2_f1_header_title',
                       'steps_to_turn_positive_s2_l2_f2_header_title', 'steps_to_turn_positive_s2_l2_f3_header_title',
                       'steps_to_turn_positive_s2_l3_button1_text', 'steps_to_turn_positive_s2_l3_button2_text',
                       'steps_to_turn_positive_s2_l3_button3_text', 'steps_to_turn_positive_s2_l3_f1_title',
                       'steps_to_turn_positive_s2_l3_f2_title', 'steps_to_turn_positive_s2_l3_f3_title']}),
        ('Power & Grace', {
            'fields': ['power_and_grace_section_1_button_text', 'power_and_grace_section_1_show_less_text',
                       'power_and_grace_s1_l1_first_field_title', 'power_and_grace_s1_l1_second_field_title',
                       'power_and_grace_s1_l1_third_field_title', 'power_and_grace_s1_l2_f1_header_title',
                       'power_and_grace_s1_l2_f2_header_title', 'power_and_grace_s1_l2_f3_header_title',
                       'power_and_grace_s1_l3_button1_text', 'power_and_grace_s1_l3_button2_text',
                       'power_and_grace_s1_l3_button3_text', 'power_and_grace_s1_l3_f1_title',
                       'power_and_grace_s1_l3_f2_title', 'power_and_grace_s1_l3_f3_title',
                       'power_and_grace_section_2_button_text', 'power_and_grace_section_2_show_less_text',
                       'power_and_grace_s2_l2_first_field_title', 'power_and_grace_s2_l2_second_field_title',
                       'power_and_grace_s2_l2_third_field_title', 'power_and_grace_s2_l2_f1_header_title',
                       'power_and_grace_s2_l2_f2_header_title', 'power_and_grace_s2_l2_f3_header_title',
                       'power_and_grace_s2_l3_button1_text', 'power_and_grace_s2_l3_button2_text',
                       'power_and_grace_s2_l3_button3_text', 'power_and_grace_s2_l3_f1_title',
                       'power_and_grace_s2_l3_f2_title', 'power_and_grace_s2_l3_f3_title']}),
        ('High Performance Ability', {
            'fields': ['high_performance_ability_section_1_button_text',
                       'high_performance_ability_section_1_show_less_text',
                       'high_performance_ability_s1_l1_first_field_title',
                       'high_performance_ability_s1_l1_second_field_title',
                       'high_performance_ability_s1_l1_third_field_title',
                       'high_performance_ability_s1_l2_f1_header_title',
                       'high_performance_ability_s1_l2_f2_header_title',
                       'high_performance_ability_s1_l2_f3_header_title',
                       'high_performance_ability_s1_l3_button1_text', 'high_performance_ability_s1_l3_button2_text',
                       'high_performance_ability_s1_l3_button3_text', 'high_performance_ability_s1_l3_f1_title',
                       'high_performance_ability_s1_l3_f2_title', 'high_performance_ability_s1_l3_f3_title',
                       'high_performance_ability_section_2_button_text',
                       'high_performance_ability_section_2_show_less_text',
                       'high_performance_ability_s2_l2_first_field_title',
                       'high_performance_ability_s2_l2_second_field_title',
                       'high_performance_ability_s2_l2_third_field_title',
                       'high_performance_ability_s2_l2_f1_header_title',
                       'high_performance_ability_s2_l2_f2_header_title',
                       'high_performance_ability_s2_l2_f3_header_title',
                       'high_performance_ability_s2_l3_button1_text', 'high_performance_ability_s2_l3_button2_text',
                       'high_performance_ability_s2_l3_button3_text', 'high_performance_ability_s2_l3_f1_title',
                       'high_performance_ability_s2_l3_f2_title', 'high_performance_ability_s2_l3_f3_title']}),
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


@admin.register(Want)
class WantAdmin(admin.ModelAdmin):
    list_filter = ('category', 'subcategory')
    list_display = (
        'name', 'category', 'subcategory'
    )
    ordering = ('order',)

    fieldsets = [
        (None, {'fields': ['name', 'category', 'subcategory', 'order']}),
        ('A Positive I Want in My Life', {
            'fields': ['positive_i_want_show_more_content_1', 'positive_i_want_show_more_content_2']}),
        ('Steps to Turn Positive', {
            'fields': ['steps_to_turn_positive_show_more_content_1', 'steps_to_turn_positive_show_more_content_2']}),
        ('Power & Grace', {
            'fields': ['power_and_grace_show_more_content_1', 'power_and_grace_show_more_content_2']}),
        ('High Performance Ability', {
            'fields': ['high_performance_ability_show_more_content_1',
                       'high_performance_ability_show_more_content_2']}),
        ('Current Habits of Ability', {
            'fields': ['current_habits_of_ability_show_more_content_1',
                       'current_habits_of_ability_show_more_content_2']}),
        ('Habit-ats Outside of Me', {
            'fields': ['habitats_outside_of_me_show_more_content_1', 'habitats_outside_of_me_show_more_content_2']}),
    ]


@admin.register(InstructionVideos)
class InstructionVideosAdmin(admin.ModelAdmin):
    list_display = (
        'want_instruction_video', 'steps_instruction_video', 'power_instruction_video',
        'ability_instruction_video', 'current_habits_instruction_video', 'habitats_instruction_video'
    )
    list_display_links = (
        'want_instruction_video', 'steps_instruction_video', 'power_instruction_video', 'ability_instruction_video',
        'current_habits_instruction_video', 'habitats_instruction_video')

    def has_add_permission(self, request):
        return not InstructionVideos.objects.exists()
