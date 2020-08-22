from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

from iow.apps.core.models import Base
from iow.apps.categories.models import Category, SubCategory


class FirstLevelContent(Base):
    show_less_content = models.CharField(
        verbose_name="Show Less Content", max_length=300, null=True)
    first_field_content = models.CharField(
        verbose_name="1st Field Content", max_length=300)
    second_field_content = models.CharField(
        verbose_name="2nd Field Content", max_length=300)
    third_field_content = models.CharField(
        verbose_name="3rd Field Content", max_length=300)

    def get_2nd_level(self):
        try:
            return SecondLevelContent.objects.get(first_level=self)
        except SecondLevelContent.DoesNotExist:
            return None
        except AttributeError:
            return None

    def __str__(self):
        return '%s' % self.show_less_content

    class Meta:
        verbose_name_plural = 'First Level Contents'
        verbose_name = 'First Level Content'


class SecondLevelContent(Base):
    first_level = models.OneToOneField(
        FirstLevelContent, verbose_name='First Level', related_name='first_and_second_level_fk',
        on_delete=models.CASCADE)

    first_f1_show_more_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    second_f1_show_more_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    third_f1_show_more_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    first_f2_show_more_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    second_f2_show_more_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    third_f2_show_more_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    first_f3_show_more_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    second_f3_show_more_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    third_f3_show_more_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    def get_3rd_level(self):
        try:
            return ThirdLevelContent.objects.get(second_level=self)
        except ThirdLevelContent.DoesNotExist:
            return None
        except AttributeError:
            return None

    def __str__(self):
        return '%s' % self.first_level

    class Meta:
        verbose_name_plural = 'Second Level Contents'
        verbose_name = 'Second Level Content'


class ThirdLevelContent(Base):
    second_level = models.OneToOneField(
        SecondLevelContent, verbose_name='Second Level', related_name='second_and_third_level_fk',
        on_delete=models.CASCADE)

    f1_1st_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f1_1st_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f1_1st_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f1_2nd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f1_2nd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f1_2nd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f1_3rd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f1_3rd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f1_3rd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    # 2nd Heading Fields
    f2_1st_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f2_1st_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f2_1st_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f2_2nd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f2_2nd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f2_2nd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f2_3rd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f2_3rd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f2_3rd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    # 3rd Heading Fields
    f3_1st_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f3_1st_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f3_1st_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f3_2nd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f3_2nd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f3_2nd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)

    f3_3rd_f1_text = models.CharField(
        verbose_name="1st Field Text", max_length=300, null=True)
    f3_3rd_f2_text = models.CharField(
        verbose_name="2nd Field Text", max_length=300, null=True)
    f3_3rd_f3_text = models.CharField(
        verbose_name="3rd Field Text", max_length=300, null=True)


    def __str__(self):
        return '%s' % self.second_level

    class Meta:
        verbose_name_plural = 'Third Level Contents'
        verbose_name = 'Third Level Content'

class Settings(Base):
    positive_i_want_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    positive_i_want_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    positive_i_want_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    positive_i_want_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    positive_i_want_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    steps_to_turn_positive_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_button1_text = models.CharField(
        verbose_name="Section 1: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_button2_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_button3_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    steps_to_turn_positive_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_button1_text = models.CharField(
        verbose_name="Section 2: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_button2_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_button3_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    steps_to_turn_positive_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    power_and_grace_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    power_and_grace_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_button1_text = models.CharField(
        verbose_name="Section 1: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_button2_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_button3_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    power_and_grace_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    power_and_grace_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_button1_text = models.CharField(
        verbose_name="Section 2: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_button2_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_button3_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    power_and_grace_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    high_performance_ability_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_button1_text = models.CharField(
        verbose_name="Section 1: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_button2_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_button3_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    high_performance_ability_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_button1_text = models.CharField(
        verbose_name="Section 2: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_button2_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_button3_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    high_performance_ability_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    current_habits_of_ability_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_button1_text = models.CharField(
        verbose_name="Section 1: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_button2_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_button3_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    current_habits_of_ability_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_button1_text = models.CharField(
        verbose_name="Section 2: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_button2_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_button3_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    current_habits_of_ability_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    habitats_outside_of_me_section_1_button_text = models.CharField(
        verbose_name="Section 1: Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_section_1_show_less_text = models.CharField(
        verbose_name="Section 1: Show Less Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l1_first_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l1_second_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l1_third_field_title = models.CharField(
        verbose_name="Section 1: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l2_f1_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l2_f2_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l2_f3_header_title = models.CharField(
        verbose_name="Section 1: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_button1_text = models.CharField(
        verbose_name="Section 1: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_button2_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_button3_text = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_f1_title = models.CharField(
        verbose_name="Section 1: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_f2_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s1_l3_f3_title = models.CharField(
        verbose_name="Section 1: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    habitats_outside_of_me_section_2_button_text = models.CharField(
        verbose_name="Section 2: Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_section_2_show_less_text = models.CharField(
        verbose_name="Section 2: Show Less Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_first_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 1st Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_second_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 2nd Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_third_field_title = models.CharField(
        verbose_name="Section 2: 1st Level: 3rd Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_f1_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 1st Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_f2_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 2nd Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l2_f3_header_title = models.CharField(
        verbose_name="Section 2: 2nd Level: 3rd Field: Header Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_button1_text = models.CharField(
        verbose_name="Section 2: 3rd Level: First Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_button2_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_button3_text = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Button Text", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_f1_title = models.CharField(
        verbose_name="Section 2: 3rd Level: First Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_f2_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Second Field Title", max_length=70, null=True, blank=True)
    habitats_outside_of_me_s2_l3_f3_title = models.CharField(
        verbose_name="Section 2: 3rd Level: Third Field Title", max_length=70, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Settings'
        verbose_name = 'Settings'

    def __str__(self):
        return 'Settings'


class Want(Base):
    name = models.CharField(max_length=200, verbose_name="Want")
    order = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, related_name='category_want', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, related_name='subcategory_want', on_delete=models.CASCADE)

    positive_i_want_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='positive_i_want_content_1',
        on_delete=models.CASCADE, null=True)
    positive_i_want_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='positive_i_want_content_2',
        on_delete=models.CASCADE, null=True)

    steps_to_turn_positive_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='steps_to_turn_positive_content_1',
        on_delete=models.CASCADE, null=True)
    steps_to_turn_positive_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='steps_to_turn_positive_content_2',
        on_delete=models.CASCADE, null=True)

    power_and_grace_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='power_and_grace_content_1',
        on_delete=models.CASCADE, null=True)
    power_and_grace_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='power_and_grace_content_2',
        on_delete=models.CASCADE, null=True)

    high_performance_ability_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='high_performance_ability_content_1',
        on_delete=models.CASCADE, null=True)
    high_performance_ability_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='high_performance_ability_content_2',
        on_delete=models.CASCADE, null=True)

    current_habits_of_ability_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='current_habits_of_ability_content_1',
        on_delete=models.CASCADE, null=True)
    current_habits_of_ability_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='current_habits_of_ability_content_2',
        on_delete=models.CASCADE, null=True)

    habitats_outside_of_me_show_more_content_1 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 1", related_name='habitats_outside_of_me_content_1',
        on_delete=models.CASCADE, null=True)
    habitats_outside_of_me_show_more_content_2 = models.ForeignKey(
        FirstLevelContent, verbose_name="Show More Content 2", related_name='habitats_outside_of_me_content_2',
        on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Wants'
        verbose_name = 'Want'

    def __str__(self):
        return '%s' % self.name

    # def get_self_benefits(self):
    #     return SelfBenefit.objects.filter(want=self)

    # def get_people_benefits(self):
    #     return PeopleBenefit.objects.filter(want=self)

    # def get_money_benefits(self):
    #     return MoneyBenefit.objects.filter(want=self)

    # def get_tasks(self):
    #     return WantCreateTask.objects.filter(want=self).order_by('idate')

    # def get_first_task(self):
    #     return WantCreateTask.objects.filter(want=self).order_by('idate')[0]

    # def get_recommended_ps(self):
    #     recommendedps = list(
    #         WantRecommendedPS.objects.filter(want=self).values_list('practicesessions', flat=True))
    #     practicesessions = PracticeSession.objects.filter(
    #         id__in=recommendedps).order_by('order')

    #     return practicesessions

    # def get_fundamental_ps(self):
    #     fundamentalps = list(
    #         FundamentalsPS.objects.filter(category=self.category, subcategory=self.subcategory).values_list('practicesessions', flat=True))
    #     practicesessions = PracticeSession.objects.filter(
    #         id__in=fundamentalps).order_by('order')

    #     return practicesessions

    # def get_why_want(self):
    #     return WhyWant.objects.filter(want=self)

    # def get_power_of_ability(self):
    #     return PowerOfAbility.objects.filter(want=self)

    # def get_grace_of_ability(self):
    #     return GraceOfAbility.objects.filter(want=self)

    # def get_what_increases_ability(self):
    #     return WhatIncreasesAbility.objects.filter(want=self).order_by('idate')

    # def get_world_class_ability(self):
    #     return WorldClassAbility.objects.filter(want=self).order_by('idate')

    # def get_obstacles_to_complete(self):
    #     return ObstaclesToComplete.objects.filter(want=self).order_by('idate')

    # def get_opportunities_to_change(self):
    #     return OpportunitiesToChange.objects.filter(want=self).order_by('idate')

    def get_absolute_url(self):
        return reverse(
            'causeandeffects_detail_specific_want',
            kwargs={
                'category': self.category.name,
                'sub_cat': self.subcategory.name,
                'want': slugify(self.name),
                'want_id': self.id
            }
        )


class InstructionVideos(Base):
    want_instruction_video = models.CharField(verbose_name="Want Instruction Video", max_length=255, null=True,
                                              blank=True)
    steps_instruction_video = models.CharField(verbose_name="3 Steps to Turn Positive Instruction Video",
                                               max_length=255, null=True,
                                               blank=True)
    power_instruction_video = models.CharField(verbose_name="Power & Grace Instruction Video", max_length=255,
                                               null=True, blank=True)
    ability_instruction_video = models.CharField(verbose_name="High Performance Ability Instruction Video",
                                                 max_length=255, null=True,
                                                 blank=True)
    current_habits_instruction_video = models.CharField(verbose_name="Current Habits of Ability Instruction Video",
                                                        max_length=255,
                                                        null=True, blank=True)
    habitats_instruction_video = models.CharField(verbose_name="Habit-ats Instruction Video", max_length=255,
                                                  null=True,
                                                  blank=True)

    class Meta:
        verbose_name_plural = 'Instruction Videos'
        verbose_name = 'Instruction Videos'

# class SelfBenefit(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_self_benefit', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Self Benefit")

#     class Meta:
#         verbose_name_plural = 'Self Benefits'
#         verbose_name = 'Self Benefit'

#     def __str__(self):
#         return '%s' % self.text

# class PeopleBenefit(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_people_benefit', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="People Benefit")

#     class Meta:
#         verbose_name_plural = 'People Benefits'
#         verbose_name = 'People Benefit'

#     def __str__(self):
#         return '%s' % self.text

# class MoneyBenefit(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_money_benefit', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Money Benefit")

#     class Meta:
#         verbose_name_plural = 'Money Benefits'
#         verbose_name = 'Money Benefit'

#     def __str__(self):
#         return '%s' % self.text

# class WantCreateTask(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_create_tasks', on_delete=models.DO_NOTHING)
#     task = models.CharField(max_length=200, verbose_name="Task to Create")
#     pos_desire = models.CharField(
#         max_length=200, verbose_name="Pos. Desire", null=True, blank=True)
#     pos_belief = models.CharField(
#         max_length=200, verbose_name="Pos. Belief", null=True, blank=True)
#     pos_expect = models.CharField(
#         max_length=200, verbose_name="Pos. Expect", null=True, blank=True)

#     class Meta:
#         verbose_name_plural = 'Tasks to Create'
#         verbose_name = 'Task to Create'

#     def __str__(self):
#         return '%s' % self.task

# class WhyWant(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_whywants', on_delete=models.DO_NOTHING)
#     name = models.CharField(max_length=200, verbose_name="Why Want")

#     class Meta:
#         verbose_name_plural = 'Why Want'
#         verbose_name = 'Why Want'

#     def __str__(self):
#         return '%s' % self.name

# class FundamentalsPS(Base):
#     category = models.ForeignKey(
#         Category, related_name='fps_category_want', on_delete=models.DO_NOTHING)
#     subcategory = models.ForeignKey(
#         SubCategory, related_name='fps_subcategory_want', on_delete=models.DO_NOTHING)
#     practicesessions = models.ManyToManyField(
#         PracticeSession, related_name='fundamental_recommended_ps')

#     class Meta:
#         verbose_name = 'Fundamental Practice Session'
#         verbose_name_plural = 'Fundamental Practice Sessions'

#     def __str__(self):
#         return '%s' % self.id

# class WantRecommendedPS(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_recommended_ps_id', on_delete=models.DO_NOTHING)
#     practicesessions = models.ManyToManyField(
#         PracticeSession, related_name='want_recommended_ps')

#     class Meta:
#         verbose_name = 'Recommended Practice Session'
#         verbose_name_plural = 'Recommended Practice Sessions'

#     def __str__(self):
#         return '%s' % self.id

# class PowerOfAbility(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_power', on_delete=models.DO_NOTHING)
#     ability = models.CharField(max_length=200, verbose_name="Ability")
#     description = models.TextField(
#         verbose_name="Ability Description", null=True, blank=True)

#     class Meta:
#         verbose_name_plural = 'Power of Abilities'
#         verbose_name = 'Power of Ability'

#     def __str__(self):
#         return '%s' % self.ability

# class GraceOfAbility(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_grace', on_delete=models.DO_NOTHING)
#     ability = models.CharField(max_length=200, verbose_name="Ability")
#     description = models.TextField(
#         verbose_name="Ability Description", null=True, blank=True)

#     class Meta:
#         verbose_name_plural = 'Grace of Abilities'
#         verbose_name = 'Grace of Ability'

#     def __str__(self):
#         return '%s' % self.ability

# class UserWant(Base):
#     user = models.ForeignKey(
#         User, related_name='why_want_user', on_delete=models.DO_NOTHING)
#     why_want = models.ForeignKey(
#         WhyWant, related_name='user_why_wants', on_delete=models.DO_NOTHING)

# class UserBenefits(Base):
#     user = models.ForeignKey(
#         User, related_name='user_user_benefits', on_delete=models.DO_NOTHING)
#     self_benefit = models.ForeignKey(SelfBenefit, related_name='user_self_benefit', on_delete=models.DO_NOTHING,
#                                      null=True)
#     people_benefit = models.ForeignKey(PeopleBenefit, related_name='people_self_benefit', on_delete=models.DO_NOTHING,
#                                        null=True)
#     money_benefit = models.ForeignKey(MoneyBenefit, related_name='money_self_benefit', on_delete=models.DO_NOTHING,
#                                       null=True)

# class UserCurrentHabit(Base):
#     user = models.ForeignKey(
#         User, related_name='user_current_habit', on_delete=models.DO_NOTHING)
#     want = models.ForeignKey(
#         Want, related_name='want_current_habit', on_delete=models.DO_NOTHING)
#     current_ability = models.CharField(
#         max_length=200, verbose_name="Current Ability")

# class WhatIncreasesAbility(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_what_increases_ability', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Text")
#     link = models.CharField(max_length=200, verbose_name="Link")

#     class Meta:
#         verbose_name_plural = 'What Increases Abilities'
#         verbose_name = 'What Increases Ability'

# class WorldClassAbility(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_world_class_ability', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Text")
#     link = models.CharField(max_length=200, verbose_name="Link")

#     class Meta:
#         verbose_name_plural = 'World Class Abilities'
#         verbose_name = 'World Class Ability'

# class ObstaclesToComplete(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_obstacles_to_complete', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Text")
#     link = models.CharField(max_length=200, verbose_name="Link")

# class OpportunitiesToChange(Base):
#     want = models.ForeignKey(
#         Want, related_name='want_opportunities_to_change', on_delete=models.DO_NOTHING)
#     text = models.CharField(max_length=200, verbose_name="Text")
#     link = models.CharField(max_length=200, verbose_name="Link")
