from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
import csv
import pdb
import xlrd
from django.core.files.storage import FileSystemStorage
from .models import Current_Reality, InstructionVideos, Settings as NegativeSettings, FirstLevelContent, SecondLevelContent, ThirdLevelContent
from iow.apps.causeandeffects.models import Want, Settings as PositiveSettings, FirstLevelContent as PositiveFirstLevelContent, SecondLevelContent as PositiveSecondLevelContent, ThirdLevelContent as PositiveThirdLevelContent 
from iow.apps.categories.models import Category, SubCategory
from django.conf import settings
import os

class CausalForces(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('order')
        sub_cats_len = []

        for category in categories:
            sub_cats_len.append(len(category.get_sub_categories()))

        max_len = max(sub_cats_len)

        table_rows = []
        for i in range(max_len):
            row = []
            for category in categories:
                try:
                    row.append({"category": category.name,
                                "sub_cat": category.get_sub_categories()[i]})
                except IndexError:
                    row.append({"category": None, "sub_cat": None})
            table_rows.append(row)

        return render(request, 'causalforces/index.html', {
            'categories': categories,
            'table_rows': table_rows,
        })


class DetailPage(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category')
        sub_cat = kwargs.get('sub_cat')
        current_reality_id = kwargs.get('current_reality_id')
        user_benefits = None

        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            category = None

        try:
            sub_cat = SubCategory.objects.get(name=sub_cat, category=category)
        except SubCategory.DoesNotExist:
            sub_cat = None

        if sub_cat:
            current_reality = None
            why_current_reality = None
            current_ability = None

            try:
                instruction_videos = InstructionVideos.objects.all()
                instruction_videos = instruction_videos[0]
            except InstructionVideos.DoesNotExist:
                instruction_videos = None
            except IndexError:
                instruction_videos = None

            try:
                negativesettings = NegativeSettings.objects.all()
                negativesettings = negativesettings[0]
            except NegativeSettings.DoesNotExist:
                negativesettings = None
            except IndexError:
                negativesettings = None

            try:
                current_realities = Current_Reality.objects.filter(
                    category=category, subcategory=sub_cat)
            except Current_Reality.DoesNotExist:
                current_realities = None

            if current_reality_id:
                try:
                    current_reality = Current_Reality.objects.get(pk=current_reality_id)
                except Current_Reality.DoesNotExist:
                    current_reality = None

            return render(request, 'causalforces/detail.html', {
                "area_of_life": category,
                "sub_area_of_life": sub_cat,
                "current_realities": current_realities,
                "current_reality": current_reality,
                "instruction_videos": instruction_videos,
                "settings": negativesettings
            })
        else:
            return render(request, 'causalforces/detail.html', {})


class detailPage_backforth(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category')
        sub_cat = kwargs.get('sub_cat')
        current_reality_id = kwargs.get('current_reality_id')
        user_benefits = None

        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            category = None

        try:
            sub_cat = SubCategory.objects.get(name=sub_cat, category=category)
        except SubCategory.DoesNotExist:
            sub_cat = None

        if sub_cat:
            current_reality = None
            why_current_reality = None
            current_ability = None

            try:
                instruction_videos = InstructionVideos.objects.all()
                instruction_videos = instruction_videos[0]
            except InstructionVideos.DoesNotExist:
                instruction_videos = None
            except IndexError:
                instruction_videos = None

            try:
                negativesettings = NegativeSettings.objects.all()
                negativesettings = negativesettings[0]
            except NegativeSettings.DoesNotExist:
                negativesettings = None
            except IndexError:
                negativesettings = None

            try:
                positivesettings = PositiveSettings.objects.all()
                positivesettings = positivesettings[0]
            except PositiveSettings.DoesNotExist:
                positivesettings = None
            except IndexError:
                positivesettings = None

            if current_reality_id:
                try:
                    current_reality = Current_Reality.objects.get(pk=current_reality_id)
                except Current_Reality.DoesNotExist:
                    current_reality = None
                

            if current_reality and current_reality.related_want:
                try:
                    num_results= Want.objects.filter(name=str(current_reality.related_want)).count()
                    if num_results:
                        want = Want.objects.filter(name=str(current_reality.related_want))[0]
                    else:
                        want=None
                except Want.DoesNotExist:
                    want = None
            else:
                want = None

            return render(request, 'causalforces/detail_backforth.html', {
                "area_of_life": category,
                "sub_area_of_life": sub_cat,
                "current_reality": current_reality,
                "want_details": want,
                "instruction_videos": instruction_videos,
                "negativesettings": negativesettings,
                "positivesettings": positivesettings
            })
        else:
            return render(request, 'causalforces/detail_backforth.html', {})



class detailPage_backforth_positive(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category')
        sub_cat = kwargs.get('sub_cat')
        want_id = kwargs.get('want_id')
        user_benefits = None

        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            category = None

        try:
            sub_cat = SubCategory.objects.get(name=sub_cat, category=category)
        except SubCategory.DoesNotExist:
            sub_cat = None

        if sub_cat:
            want = None
            why_wants = None
            current_ability = None

            try:
                instruction_videos = InstructionVideos.objects.all()
                instruction_videos = instruction_videos[0]
            except InstructionVideos.DoesNotExist:
                instruction_videos = None
            except IndexError:
                instruction_videos = None

            try:
                negativesettings = NegativeSettings.objects.all()
                negativesettings = negativesettings[0]
            except NegativeSettings.DoesNotExist:
                negativesettings = None
            except IndexError:
                negativesettings = None

            try:
                positivesettings = PositiveSettings.objects.all()
                positivesettings = positivesettings[0]
            except PositiveSettings.DoesNotExist:
                positivesettings = None
            except IndexError:
                positivesettings = None

            if want_id:
                try:
                    want = Want.objects.get(pk=want_id)
                except Want.DoesNotExist:
                    want = None
            if want:
                try:
                    num_results= Current_Reality.objects.filter(related_want=want_id).count()
                    if num_results:
                        current_reality = Current_Reality.objects.filter(related_want=want_id)[0]
                    else:
                        current_reality = None
                except Current_Reality.DoesNotExist:
                    current_reality = None
            return render(request, 'causalforces/detail_backforth.html', {
                "area_of_life": category,
                "sub_area_of_life": sub_cat,
                "current_reality": current_reality,
                "want_details": want,
                "instruction_videos": instruction_videos,
                "negativesettings": negativesettings,
                "positivesettings": positivesettings
            })
        else:
            return render(request, 'causalforces/detail_backforth.html', {})


class connect_excel_file(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
            return render(request, "causalforces/uploadcsv.html")

    def post(self, request, *args, **kwargs):
        data=[]
        Errors=[]
        warning=[]
        Success=[]
        valuecheck=False
        if request.method=='POST' and request.FILES['csv_file']:
            try:
                csv_file = request.FILES["csv_file"]
                fs=FileSystemStorage()
                filename=fs.save(csv_file.name, csv_file)
                uploaded_file_url = fs.url(filename)
                media_url = settings.MEDIA_URL
                delete_file=os.path.join("%s\%s" % (settings.MEDIA_ROOT, csv_file))
                try:
                    workbook = xlrd.open_workbook(delete_file, on_demand = True)
                    worksheet = workbook.sheet_by_index(0)
                    
                    try:
                        category_check = Category.objects.filter(name=worksheet.cell_value(0,1))
                        if category_check:
                            category_save = Category.objects.filter(name=worksheet.cell_value(0,1))[0]
                        if not category_check:
                            try:
                                if worksheet.cell_value(0,3) != "":
                                    category_save = Category.objects.create(name=worksheet.cell_value(0,1), order=worksheet.cell_value(0,3))
                            except:
                                valuecheck=True 
                                Errors.append("Area order field is empty")
                    except:
                        valuecheck=True 
                        Errors.append("Area name field is empty" )
                    try:
                        sub_category_check = SubCategory.objects.filter(category=category_save, name=worksheet.cell_value(1,1))
                        if sub_category_check:
                            sub_category_save = SubCategory.objects.filter(category=category_save, name=worksheet.cell_value(1,1))[0]
                        if not sub_category_check:
                            try:
                                if worksheet.cell_value(1,3)!= "":
                                    sub_category_save = SubCategory.objects.create(category=category_save, name=worksheet.cell_value(1,1), order=worksheet.cell_value(1,3))
                            except:
                                valuecheck=True  
                                Errors.append("Sub Area order field is empty")
                    except:
                        valuecheck=True
                        Errors.append("Sub Area name field is empty")

                    '''try:
                        want_check1 = Want.objects.filter(name=worksheet.cell_value(2,6), category=category_save, subcategory=sub_category_save)
                        if want_check1:
                            want_save1 = Want.objects.filter(name=worksheet.cell_value(2,6), category=category_save, subcategory=sub_category_save)[0]
                        if not want_check1:
                            try:
                                if worksheet.cell_value(2,8)!= "":
                                    print('')
                            except:
                                valuecheck=True  
                                Errors.append("Want order field is empty")
                    except:
                        valuecheck=True 
                        Errors.append("Want name field is empty")
                    try:
                        current_reality_check1 = Current_Reality.objects.filter(name=worksheet.cell_value(2,1))
                        if current_reality_check1:
                            current_reality_save1 = Current_Reality.objects.filter(name=worksheet.cell_value(2,1))[0]
                        if not current_reality_check1:
                            try:
                                if worksheet.cell_value(2,3)!= "":
                                    print('')
                            except:
                                valuecheck=True  
                                Errors.append("Current Reality order field is empty")
                    except:
                        valuecheck=True 
                        Errors.append("Current Reality name field is empty")'''

                    try:
                        if worksheet.cell_value(8,6)== "" or worksheet.cell_value(24,6)== "" or worksheet.cell_value(42,6)== "" or worksheet.cell_value(58,6)== "" or worksheet.cell_value(76,6)== "" or worksheet.cell_value(92,6)== "" or worksheet.cell_value(110,6)== "" or worksheet.cell_value(126,6)== "" or worksheet.cell_value(160,6)== "" or worksheet.cell_value(178,6)== "" or worksheet.cell_value(194,6)== "" or worksheet.cell_value(8,1)== "" or worksheet.cell_value(24,1)== "" or worksheet.cell_value(42,1)== "" or worksheet.cell_value(58,1)== "" or worksheet.cell_value(76,1)== "" or worksheet.cell_value(92,1)== "" or worksheet.cell_value(110,1)== "" or worksheet.cell_value(126,1)== "" or worksheet.cell_value(144,1)== "" or worksheet.cell_value(160,1)== ""or worksheet.cell_value(178,1)== ""or worksheet.cell_value(194,1)== "":
                            valuecheck=True  
                            Errors.append("Please make sure of first values of first level Contents")
                    except:
                        Errors.append("First Level values couldn't be evaluated")
                    
                    
                    if valuecheck==False:
                        try:
                            positive_positive1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(8,6), first_field_content=worksheet.cell_value(9,6), second_field_content=worksheet.cell_value(14,6), third_field_content=worksheet.cell_value(19,6))
                            if positive_positive1_first_level_check:
                                positive_positive1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(8,6), first_field_content=worksheet.cell_value(9,6), second_field_content=worksheet.cell_value(14,6), third_field_content=worksheet.cell_value(19,6))[0]
                            else:
                                positive_positive1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(8,6), first_field_content=worksheet.cell_value(9,6), second_field_content=worksheet.cell_value(14,6), third_field_content=worksheet.cell_value(19,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Negative First Level values") 
                        
                        try:
                            positive_positive2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(24,6), first_field_content=worksheet.cell_value(25,6), second_field_content=worksheet.cell_value(30,6), third_field_content=worksheet.cell_value(35,6))
                            if positive_positive2_first_level_check:
                                positive_positive2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(24,6), first_field_content=worksheet.cell_value(25,6), second_field_content=worksheet.cell_value(30,6), third_field_content=worksheet.cell_value(35,6))[0]
                            else:
                                positive_positive2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(24,6), first_field_content=worksheet.cell_value(25,6), second_field_content=worksheet.cell_value(30,6), third_field_content=worksheet.cell_value(35,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Negative First Level values")
                        
                        try:
                            positive_steps1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(42,6), first_field_content=worksheet.cell_value(43,6), second_field_content=worksheet.cell_value(48,6), third_field_content=worksheet.cell_value(53,6))
                            if positive_steps1_first_level_check:
                                positive_steps1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(42,6), first_field_content=worksheet.cell_value(43,6), second_field_content=worksheet.cell_value(48,6), third_field_content=worksheet.cell_value(53,6))[0]
                            else:
                                positive_steps1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(42,6), first_field_content=worksheet.cell_value(43,6), second_field_content=worksheet.cell_value(48,6), third_field_content=worksheet.cell_value(53,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Steps First Level values")
                        
                        try:
                            positive_steps2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(58,6), first_field_content=worksheet.cell_value(59,6), second_field_content=worksheet.cell_value(64,6), third_field_content=worksheet.cell_value(69,6))
                            if positive_steps2_first_level_check:
                                positive_steps2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(58,6), first_field_content=worksheet.cell_value(59,6), second_field_content=worksheet.cell_value(64,6), third_field_content=worksheet.cell_value(69,6))[0]
                            else:
                                positive_steps2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(58,6), first_field_content=worksheet.cell_value(59,6), second_field_content=worksheet.cell_value(64,6), third_field_content=worksheet.cell_value(69,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Steps First Level values")
                        
                        try:
                            positive_power1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(76,6), first_field_content=worksheet.cell_value(77,6), second_field_content=worksheet.cell_value(82,6), third_field_content=worksheet.cell_value(87,6))
                            if positive_power1_first_level_check:
                                positive_power1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(76,6), first_field_content=worksheet.cell_value(77,6), second_field_content=worksheet.cell_value(82,6), third_field_content=worksheet.cell_value(87,6))[0]
                            else:
                                positive_power1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(76,6), first_field_content=worksheet.cell_value(77,6), second_field_content=worksheet.cell_value(82,6), third_field_content=worksheet.cell_value(87,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Weak First Level values")
                        
                        try:
                            positive_power2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(92,6), first_field_content=worksheet.cell_value(93,6), second_field_content=worksheet.cell_value(98,6), third_field_content=worksheet.cell_value(103,6))
                            if positive_power2_first_level_check:
                                positive_power2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(92,6), first_field_content=worksheet.cell_value(93,6), second_field_content=worksheet.cell_value(98,6), third_field_content=worksheet.cell_value(103,6))[0]
                            else:
                                positive_power2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(92,6), first_field_content=worksheet.cell_value(93,6), second_field_content=worksheet.cell_value(98,6), third_field_content=worksheet.cell_value(103,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Weak First Level values")
                        
                        try:
                            positive_high1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(110,6), first_field_content=worksheet.cell_value(111,6), second_field_content=worksheet.cell_value(116,6), third_field_content=worksheet.cell_value(121,6))
                            if positive_high1_first_level_check:
                                positive_high1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(110,6), first_field_content=worksheet.cell_value(111,6), second_field_content=worksheet.cell_value(116,6), third_field_content=worksheet.cell_value(121,6))[0]
                            else:
                                positive_high1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(110,6), first_field_content=worksheet.cell_value(111,6), second_field_content=worksheet.cell_value(116,6), third_field_content=worksheet.cell_value(121,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Low First Level values")
                        
                        try:
                            positive_high2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(126,6), first_field_content=worksheet.cell_value(127,6), second_field_content=worksheet.cell_value(132,6), third_field_content=worksheet.cell_value(137,6))
                            if positive_high2_first_level_check:
                                positive_high2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(126,6), first_field_content=worksheet.cell_value(127,6), second_field_content=worksheet.cell_value(132,6), third_field_content=worksheet.cell_value(137,6))[0]
                            else:
                                positive_high2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(126,6), first_field_content=worksheet.cell_value(127,6), second_field_content=worksheet.cell_value(132,6), third_field_content=worksheet.cell_value(137,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Low First Level values")
                        
                        try:
                            positive_current1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(144,6), first_field_content=worksheet.cell_value(145,6), second_field_content=worksheet.cell_value(150,6), third_field_content=worksheet.cell_value(155,6))
                            if positive_current1_first_level_check:
                                positive_current1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(144,6), first_field_content=worksheet.cell_value(145,6), second_field_content=worksheet.cell_value(150,6), third_field_content=worksheet.cell_value(155,6))[0]
                            else:
                                positive_current1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(144,6), first_field_content=worksheet.cell_value(145,6), second_field_content=worksheet.cell_value(150,6), third_field_content=worksheet.cell_value(155,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Current First Level values")
                        
                        try:
                            positive_current2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(160,6), first_field_content=worksheet.cell_value(161,6), second_field_content=worksheet.cell_value(166,6), third_field_content=worksheet.cell_value(171,6))
                            if positive_current2_first_level_check:
                                positive_current2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(160,6), first_field_content=worksheet.cell_value(161,6), second_field_content=worksheet.cell_value(166,6), third_field_content=worksheet.cell_value(171,6))[0]
                            else:
                                positive_current2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(160,6), first_field_content=worksheet.cell_value(161,6), second_field_content=worksheet.cell_value(166,6), third_field_content=worksheet.cell_value(171,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Current First Level values")
                        
                        try:
                            positive_habitats1_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(178,6), first_field_content=worksheet.cell_value(179,6), second_field_content=worksheet.cell_value(184,6), third_field_content=worksheet.cell_value(189,6))
                            if positive_habitats1_first_level_check:
                                positive_habitats1_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(178,6), first_field_content=worksheet.cell_value(179,6), second_field_content=worksheet.cell_value(184,6), third_field_content=worksheet.cell_value(189,6))[0]
                            else:
                                positive_habitats1_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(178,6), first_field_content=worksheet.cell_value(179,6), second_field_content=worksheet.cell_value(184,6), third_field_content=worksheet.cell_value(189,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Habitats First Level values")
                        
                        try:
                            positive_habitats2_first_level_check = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(194,6), first_field_content=worksheet.cell_value(195,6), second_field_content=worksheet.cell_value(200,6), third_field_content=worksheet.cell_value(205,6))
                            if positive_habitats2_first_level_check:
                                positive_habitats2_first_level_save = PositiveFirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(194,6), first_field_content=worksheet.cell_value(195,6), second_field_content=worksheet.cell_value(200,6), third_field_content=worksheet.cell_value(205,6))[0]
                            else:
                                positive_habitats2_first_level_save = PositiveFirstLevelContent.objects.create(show_less_content=worksheet.cell_value(194,6), first_field_content=worksheet.cell_value(195,6), second_field_content=worksheet.cell_value(200,6), third_field_content=worksheet.cell_value(205,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Habitats First Level values")
                        
                        try:
                            positive_positive1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_positive1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,6), second_f1_show_more_text=worksheet.cell_value(11,6), third_f1_show_more_text=worksheet.cell_value(12,6), first_f2_show_more_text=worksheet.cell_value(15,6), second_f2_show_more_text=worksheet.cell_value(16,6), third_f2_show_more_text=worksheet.cell_value(17,6), first_f3_show_more_text=worksheet.cell_value(20,6), second_f3_show_more_text=worksheet.cell_value(21,6), third_f3_show_more_text=worksheet.cell_value(22,6))
                            if positive_positive1_second_level_check:
                                positive_positive1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_positive1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,6), second_f1_show_more_text=worksheet.cell_value(11,6), third_f1_show_more_text=worksheet.cell_value(12,6), first_f2_show_more_text=worksheet.cell_value(15,6), second_f2_show_more_text=worksheet.cell_value(16,6), third_f2_show_more_text=worksheet.cell_value(17,6), first_f3_show_more_text=worksheet.cell_value(20,6), second_f3_show_more_text=worksheet.cell_value(21,6), third_f3_show_more_text=worksheet.cell_value(22,6))[0]
                            else:
                                positive_positive1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_positive1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,6), second_f1_show_more_text=worksheet.cell_value(11,6), third_f1_show_more_text=worksheet.cell_value(12,6), first_f2_show_more_text=worksheet.cell_value(15,6), second_f2_show_more_text=worksheet.cell_value(16,6), third_f2_show_more_text=worksheet.cell_value(17,6), first_f3_show_more_text=worksheet.cell_value(20,6), second_f3_show_more_text=worksheet.cell_value(21,6), third_f3_show_more_text=worksheet.cell_value(22,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Negative Second Level values")
                        
                        try:
                            positive_positive2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_positive2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,6), second_f1_show_more_text=worksheet.cell_value(27,6), third_f1_show_more_text=worksheet.cell_value(28,6), first_f2_show_more_text=worksheet.cell_value(31,6), second_f2_show_more_text=worksheet.cell_value(32,6), third_f2_show_more_text=worksheet.cell_value(33,6), first_f3_show_more_text=worksheet.cell_value(36,6), second_f3_show_more_text=worksheet.cell_value(37,6), third_f3_show_more_text=worksheet.cell_value(38,6))
                            if positive_positive2_second_level_check:
                                positive_positive2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_positive2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,6), second_f1_show_more_text=worksheet.cell_value(27,6), third_f1_show_more_text=worksheet.cell_value(28,6), first_f2_show_more_text=worksheet.cell_value(31,6), second_f2_show_more_text=worksheet.cell_value(32,6), third_f2_show_more_text=worksheet.cell_value(33,6), first_f3_show_more_text=worksheet.cell_value(36,6), second_f3_show_more_text=worksheet.cell_value(37,6), third_f3_show_more_text=worksheet.cell_value(38,6))[0]
                            else:
                                positive_positive2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_positive2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,6), second_f1_show_more_text=worksheet.cell_value(27,6), third_f1_show_more_text=worksheet.cell_value(28,6), first_f2_show_more_text=worksheet.cell_value(31,6), second_f2_show_more_text=worksheet.cell_value(32,6), third_f2_show_more_text=worksheet.cell_value(33,6), first_f3_show_more_text=worksheet.cell_value(36,6), second_f3_show_more_text=worksheet.cell_value(37,6), third_f3_show_more_text=worksheet.cell_value(38,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Negative Second Level values")
                        
                        try:
                            positive_steps1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,6), second_f1_show_more_text=worksheet.cell_value(45,6), third_f1_show_more_text=worksheet.cell_value(46,6), first_f2_show_more_text=worksheet.cell_value(49,6), second_f2_show_more_text=worksheet.cell_value(50,6), third_f2_show_more_text=worksheet.cell_value(51,6), first_f3_show_more_text=worksheet.cell_value(54,6), second_f3_show_more_text=worksheet.cell_value(55,6), third_f3_show_more_text=worksheet.cell_value(56,6))
                            if positive_steps1_second_level_check:
                                positive_steps1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,6), second_f1_show_more_text=worksheet.cell_value(45,6), third_f1_show_more_text=worksheet.cell_value(46,6), first_f2_show_more_text=worksheet.cell_value(49,6), second_f2_show_more_text=worksheet.cell_value(50,6), third_f2_show_more_text=worksheet.cell_value(51,6), first_f3_show_more_text=worksheet.cell_value(54,6), second_f3_show_more_text=worksheet.cell_value(55,6), third_f3_show_more_text=worksheet.cell_value(56,6))[0]
                            else:
                                positive_steps1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,6), second_f1_show_more_text=worksheet.cell_value(45,6), third_f1_show_more_text=worksheet.cell_value(46,6), first_f2_show_more_text=worksheet.cell_value(49,6), second_f2_show_more_text=worksheet.cell_value(50,6), third_f2_show_more_text=worksheet.cell_value(51,6), first_f3_show_more_text=worksheet.cell_value(54,6), second_f3_show_more_text=worksheet.cell_value(55,6), third_f3_show_more_text=worksheet.cell_value(56,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Steps Second Level values")
                        
                        try:
                            positive_steps2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,6), second_f1_show_more_text=worksheet.cell_value(61,6), third_f1_show_more_text=worksheet.cell_value(62,6), first_f2_show_more_text=worksheet.cell_value(65,6), second_f2_show_more_text=worksheet.cell_value(66,6), third_f2_show_more_text=worksheet.cell_value(67,6), first_f3_show_more_text=worksheet.cell_value(70,6), second_f3_show_more_text=worksheet.cell_value(71,6), third_f3_show_more_text=worksheet.cell_value(72,6))
                            if positive_steps2_second_level_check:
                                positive_steps2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,6), second_f1_show_more_text=worksheet.cell_value(61,6), third_f1_show_more_text=worksheet.cell_value(62,6), first_f2_show_more_text=worksheet.cell_value(65,6), second_f2_show_more_text=worksheet.cell_value(66,6), third_f2_show_more_text=worksheet.cell_value(67,6), first_f3_show_more_text=worksheet.cell_value(70,6), second_f3_show_more_text=worksheet.cell_value(71,6), third_f3_show_more_text=worksheet.cell_value(72,6))[0]
                            else:
                                positive_steps2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,6), second_f1_show_more_text=worksheet.cell_value(61,6), third_f1_show_more_text=worksheet.cell_value(62,6), first_f2_show_more_text=worksheet.cell_value(65,6), second_f2_show_more_text=worksheet.cell_value(66,6), third_f2_show_more_text=worksheet.cell_value(67,6), first_f3_show_more_text=worksheet.cell_value(70,6), second_f3_show_more_text=worksheet.cell_value(71,6), third_f3_show_more_text=worksheet.cell_value(72,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Steps Second Level values")
                        
                        try:
                            positive_power1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_power1_first_level_save,first_f1_show_more_text=worksheet.cell_value(78,6), second_f1_show_more_text=worksheet.cell_value(79,6), third_f1_show_more_text=worksheet.cell_value(80,6), first_f2_show_more_text=worksheet.cell_value(83,6), second_f2_show_more_text=worksheet.cell_value(84,6), third_f2_show_more_text=worksheet.cell_value(85,6), first_f3_show_more_text=worksheet.cell_value(88,6), second_f3_show_more_text=worksheet.cell_value(89,6), third_f3_show_more_text=worksheet.cell_value(90,6))
                            if positive_power1_second_level_check:
                                positive_power1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_power1_first_level_save, first_f1_show_more_text=worksheet.cell_value(78,6), second_f1_show_more_text=worksheet.cell_value(79,6), third_f1_show_more_text=worksheet.cell_value(80,6), first_f2_show_more_text=worksheet.cell_value(83,6), second_f2_show_more_text=worksheet.cell_value(84,6), third_f2_show_more_text=worksheet.cell_value(85,6), first_f3_show_more_text=worksheet.cell_value(88,6), second_f3_show_more_text=worksheet.cell_value(89,6), third_f3_show_more_text=worksheet.cell_value(90,6))[0]
                            else:
                                positive_power1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_power1_first_level_save, first_f1_show_more_text=worksheet.cell_value(78,6), second_f1_show_more_text=worksheet.cell_value(79,6), third_f1_show_more_text=worksheet.cell_value(80,6), first_f2_show_more_text=worksheet.cell_value(83,6), second_f2_show_more_text=worksheet.cell_value(84,6), third_f2_show_more_text=worksheet.cell_value(85,6), first_f3_show_more_text=worksheet.cell_value(88,6), second_f3_show_more_text=worksheet.cell_value(89,6), third_f3_show_more_text=worksheet.cell_value(90,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Weak Second Level values")
                        
                        try:
                            positive_power2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_power2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,6), second_f1_show_more_text=worksheet.cell_value(95,6), third_f1_show_more_text=worksheet.cell_value(96,6), first_f2_show_more_text=worksheet.cell_value(99,6), second_f2_show_more_text=worksheet.cell_value(100,6), third_f2_show_more_text=worksheet.cell_value(101,6), first_f3_show_more_text=worksheet.cell_value(104,6), second_f3_show_more_text=worksheet.cell_value(105,6), third_f3_show_more_text=worksheet.cell_value(106,6))
                            if positive_power2_second_level_check:
                                positive_power2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_power2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,6), second_f1_show_more_text=worksheet.cell_value(95,6), third_f1_show_more_text=worksheet.cell_value(96,6), first_f2_show_more_text=worksheet.cell_value(99,6), second_f2_show_more_text=worksheet.cell_value(100,6), third_f2_show_more_text=worksheet.cell_value(101,6), first_f3_show_more_text=worksheet.cell_value(104,6), second_f3_show_more_text=worksheet.cell_value(105,6), third_f3_show_more_text=worksheet.cell_value(106,6))[0]
                            else:
                                positive_power2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_power2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,6), second_f1_show_more_text=worksheet.cell_value(95,6), third_f1_show_more_text=worksheet.cell_value(96,6), first_f2_show_more_text=worksheet.cell_value(99,6), second_f2_show_more_text=worksheet.cell_value(100,6), third_f2_show_more_text=worksheet.cell_value(101,6), first_f3_show_more_text=worksheet.cell_value(104,6), second_f3_show_more_text=worksheet.cell_value(105,6), third_f3_show_more_text=worksheet.cell_value(106,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Weak Second Level values")
                        
                        try:
                            positive_high1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_high1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,6), second_f1_show_more_text=worksheet.cell_value(113,6), third_f1_show_more_text=worksheet.cell_value(114,6), first_f2_show_more_text=worksheet.cell_value(117,6), second_f2_show_more_text=worksheet.cell_value(118,6), third_f2_show_more_text=worksheet.cell_value(119,6), first_f3_show_more_text=worksheet.cell_value(122,6), second_f3_show_more_text=worksheet.cell_value(123,6), third_f3_show_more_text=worksheet.cell_value(124,6))
                            if positive_high1_second_level_check:
                                positive_high1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_high1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,6), second_f1_show_more_text=worksheet.cell_value(113,6), third_f1_show_more_text=worksheet.cell_value(114,6), first_f2_show_more_text=worksheet.cell_value(117,6), second_f2_show_more_text=worksheet.cell_value(118,6), third_f2_show_more_text=worksheet.cell_value(119,6), first_f3_show_more_text=worksheet.cell_value(122,6), second_f3_show_more_text=worksheet.cell_value(123,6), third_f3_show_more_text=worksheet.cell_value(124,6))[0]
                            else:
                                positive_high1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_high1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,6), second_f1_show_more_text=worksheet.cell_value(113,6), third_f1_show_more_text=worksheet.cell_value(114,6), first_f2_show_more_text=worksheet.cell_value(117,6), second_f2_show_more_text=worksheet.cell_value(118,6), third_f2_show_more_text=worksheet.cell_value(119,6), first_f3_show_more_text=worksheet.cell_value(122,6), second_f3_show_more_text=worksheet.cell_value(123,6), third_f3_show_more_text=worksheet.cell_value(124,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Low Second Level values")
                        
                        try:
                            positive_high2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_high2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,6), second_f1_show_more_text=worksheet.cell_value(129,6), third_f1_show_more_text=worksheet.cell_value(130,6), first_f2_show_more_text=worksheet.cell_value(133,6), second_f2_show_more_text=worksheet.cell_value(134,6), third_f2_show_more_text=worksheet.cell_value(135,6), first_f3_show_more_text=worksheet.cell_value(138,6), second_f3_show_more_text=worksheet.cell_value(139,6), third_f3_show_more_text=worksheet.cell_value(140,6))
                            if positive_high2_second_level_check:
                                positive_high2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_high2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,6), second_f1_show_more_text=worksheet.cell_value(129,6), third_f1_show_more_text=worksheet.cell_value(130,6), first_f2_show_more_text=worksheet.cell_value(133,6), second_f2_show_more_text=worksheet.cell_value(134,6), third_f2_show_more_text=worksheet.cell_value(135,6), first_f3_show_more_text=worksheet.cell_value(138,6), second_f3_show_more_text=worksheet.cell_value(139,6), third_f3_show_more_text=worksheet.cell_value(140,6))[0]
                            else:
                                positive_high2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_high2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,6), second_f1_show_more_text=worksheet.cell_value(129,6), third_f1_show_more_text=worksheet.cell_value(130,6), first_f2_show_more_text=worksheet.cell_value(133,6), second_f2_show_more_text=worksheet.cell_value(134,6), third_f2_show_more_text=worksheet.cell_value(135,6), first_f3_show_more_text=worksheet.cell_value(138,6), second_f3_show_more_text=worksheet.cell_value(139,6), third_f3_show_more_text=worksheet.cell_value(140,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Low Second Level values")
                        
                        try:
                            positive_current1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,6), second_f1_show_more_text=worksheet.cell_value(147,6), third_f1_show_more_text=worksheet.cell_value(148,6), first_f2_show_more_text=worksheet.cell_value(151,6), second_f2_show_more_text=worksheet.cell_value(152,6), third_f2_show_more_text=worksheet.cell_value(153,6), first_f3_show_more_text=worksheet.cell_value(156,6), second_f3_show_more_text=worksheet.cell_value(157,6), third_f3_show_more_text=worksheet.cell_value(158,6))
                            if positive_current1_second_level_check:
                                positive_current1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,6), second_f1_show_more_text=worksheet.cell_value(147,6), third_f1_show_more_text=worksheet.cell_value(148,6), first_f2_show_more_text=worksheet.cell_value(151,6), second_f2_show_more_text=worksheet.cell_value(152,6), third_f2_show_more_text=worksheet.cell_value(153,6), first_f3_show_more_text=worksheet.cell_value(156,6), second_f3_show_more_text=worksheet.cell_value(157,6), third_f3_show_more_text=worksheet.cell_value(158,6))[0]
                            else:
                                positive_current1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,6), second_f1_show_more_text=worksheet.cell_value(147,6), third_f1_show_more_text=worksheet.cell_value(148,6), first_f2_show_more_text=worksheet.cell_value(151,6), second_f2_show_more_text=worksheet.cell_value(152,6), third_f2_show_more_text=worksheet.cell_value(153,6), first_f3_show_more_text=worksheet.cell_value(156,6), second_f3_show_more_text=worksheet.cell_value(157,6), third_f3_show_more_text=worksheet.cell_value(158,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Current Second Level values")
                        
                        try:
                            positive_current2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,6), second_f1_show_more_text=worksheet.cell_value(163,6), third_f1_show_more_text=worksheet.cell_value(164,6), first_f2_show_more_text=worksheet.cell_value(167,6), second_f2_show_more_text=worksheet.cell_value(168,6), third_f2_show_more_text=worksheet.cell_value(169,6), first_f3_show_more_text=worksheet.cell_value(172,6), second_f3_show_more_text=worksheet.cell_value(173,6), third_f3_show_more_text=worksheet.cell_value(174,6))
                            if positive_current2_second_level_check:
                                positive_current2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,6), second_f1_show_more_text=worksheet.cell_value(163,6), third_f1_show_more_text=worksheet.cell_value(164,6), first_f2_show_more_text=worksheet.cell_value(167,6), second_f2_show_more_text=worksheet.cell_value(168,6), third_f2_show_more_text=worksheet.cell_value(169,6), first_f3_show_more_text=worksheet.cell_value(172,6), second_f3_show_more_text=worksheet.cell_value(173,6), third_f3_show_more_text=worksheet.cell_value(174,6))[0]
                            else:
                                positive_current2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,6), second_f1_show_more_text=worksheet.cell_value(163,6), third_f1_show_more_text=worksheet.cell_value(164,6), first_f2_show_more_text=worksheet.cell_value(167,6), second_f2_show_more_text=worksheet.cell_value(168,6), third_f2_show_more_text=worksheet.cell_value(169,6), first_f3_show_more_text=worksheet.cell_value(172,6), second_f3_show_more_text=worksheet.cell_value(173,6), third_f3_show_more_text=worksheet.cell_value(174,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Current Second Level values")
                        
                        try:
                            positive_habitats1_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,6), second_f1_show_more_text=worksheet.cell_value(181,6), third_f1_show_more_text=worksheet.cell_value(182,6), first_f2_show_more_text=worksheet.cell_value(185,6), second_f2_show_more_text=worksheet.cell_value(186,6), third_f2_show_more_text=worksheet.cell_value(187,6), first_f3_show_more_text=worksheet.cell_value(190,6), second_f3_show_more_text=worksheet.cell_value(191,6), third_f3_show_more_text=worksheet.cell_value(192,6))
                            if positive_habitats1_second_level_check:
                                positive_habitats1_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,6), second_f1_show_more_text=worksheet.cell_value(181,6), third_f1_show_more_text=worksheet.cell_value(182,6), first_f2_show_more_text=worksheet.cell_value(185,6), second_f2_show_more_text=worksheet.cell_value(186,6), third_f2_show_more_text=worksheet.cell_value(187,6), first_f3_show_more_text=worksheet.cell_value(190,6), second_f3_show_more_text=worksheet.cell_value(191,6), third_f3_show_more_text=worksheet.cell_value(192,6))[0]
                            else:
                                positive_habitats1_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,6), second_f1_show_more_text=worksheet.cell_value(181,6), third_f1_show_more_text=worksheet.cell_value(182,6), first_f2_show_more_text=worksheet.cell_value(185,6), second_f2_show_more_text=worksheet.cell_value(186,6), third_f2_show_more_text=worksheet.cell_value(187,6), first_f3_show_more_text=worksheet.cell_value(190,6), second_f3_show_more_text=worksheet.cell_value(191,6), third_f3_show_more_text=worksheet.cell_value(192,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Habitats Second Level values")
                        
                        try:
                            positive_habitats2_second_level_check =PositiveSecondLevelContent.objects.filter(first_level=positive_habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,6), second_f1_show_more_text=worksheet.cell_value(197,6), third_f1_show_more_text=worksheet.cell_value(198,6), first_f2_show_more_text=worksheet.cell_value(201,6), second_f2_show_more_text=worksheet.cell_value(202,6), third_f2_show_more_text=worksheet.cell_value(203,6), first_f3_show_more_text=worksheet.cell_value(206,6), second_f3_show_more_text=worksheet.cell_value(207,6), third_f3_show_more_text=worksheet.cell_value(208,6))
                            if positive_habitats2_second_level_check:
                                positive_habitats2_second_level_save =PositiveSecondLevelContent.objects.filter(first_level=positive_habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,6), second_f1_show_more_text=worksheet.cell_value(197,6), third_f1_show_more_text=worksheet.cell_value(198,6), first_f2_show_more_text=worksheet.cell_value(201,6), second_f2_show_more_text=worksheet.cell_value(202,6), third_f2_show_more_text=worksheet.cell_value(203,6), first_f3_show_more_text=worksheet.cell_value(206,6), second_f3_show_more_text=worksheet.cell_value(207,6), third_f3_show_more_text=worksheet.cell_value(208,6))[0]
                            else:
                                positive_habitats2_second_level_save =PositiveSecondLevelContent.objects.create(first_level=positive_habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,6), second_f1_show_more_text=worksheet.cell_value(197,6), third_f1_show_more_text=worksheet.cell_value(198,6), first_f2_show_more_text=worksheet.cell_value(201,6), second_f2_show_more_text=worksheet.cell_value(202,6), third_f2_show_more_text=worksheet.cell_value(203,6), first_f3_show_more_text=worksheet.cell_value(206,6), second_f3_show_more_text=worksheet.cell_value(207,6), third_f3_show_more_text=worksheet.cell_value(208,6))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Habitats Second Level values")
                        
                        try:
                            positive_positive1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_positive1_second_level_save,  f1_1st_f1_text=worksheet.cell_value(10,7), f1_1st_f2_text=worksheet.cell_value(10,8), f1_1st_f3_text=worksheet.cell_value(10,9), f1_2nd_f1_text=worksheet.cell_value(11,7), f1_2nd_f2_text=worksheet.cell_value(11,8), f1_2nd_f3_text=worksheet.cell_value(11,9), f1_3rd_f1_text=worksheet.cell_value(12,7), f1_3rd_f2_text=worksheet.cell_value(12,8), f1_3rd_f3_text=worksheet.cell_value(12,9), f2_1st_f1_text=worksheet.cell_value(15,7), f2_1st_f2_text=worksheet.cell_value(15,8), f2_1st_f3_text=worksheet.cell_value(15,9), f2_2nd_f1_text=worksheet.cell_value(16,7), f2_2nd_f2_text=worksheet.cell_value(16,8), f2_2nd_f3_text=worksheet.cell_value(16,9), f2_3rd_f1_text=worksheet.cell_value(17,7), f2_3rd_f2_text=worksheet.cell_value(17,8), f2_3rd_f3_text=worksheet.cell_value(17,9), f3_1st_f1_text=worksheet.cell_value(20,7), f3_1st_f2_text=worksheet.cell_value(20,8), f3_1st_f3_text=worksheet.cell_value(20,9), f3_2nd_f1_text=worksheet.cell_value(21,7), f3_2nd_f2_text=worksheet.cell_value(21,8), f3_2nd_f3_text=worksheet.cell_value(21,9), f3_3rd_f1_text=worksheet.cell_value(22,7), f3_3rd_f2_text=worksheet.cell_value(22,8), f3_3rd_f3_text=worksheet.cell_value(22,9))
                            if positive_positive1_third_level_check:
                                positive_positive1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_positive1_second_level_save, f1_1st_f1_text=worksheet.cell_value(10,7), f1_1st_f2_text=worksheet.cell_value(10,8), f1_1st_f3_text=worksheet.cell_value(10,9), f1_2nd_f1_text=worksheet.cell_value(11,7), f1_2nd_f2_text=worksheet.cell_value(11,8), f1_2nd_f3_text=worksheet.cell_value(11,9), f1_3rd_f1_text=worksheet.cell_value(12,7), f1_3rd_f2_text=worksheet.cell_value(12,8), f1_3rd_f3_text=worksheet.cell_value(12,9), f2_1st_f1_text=worksheet.cell_value(15,7), f2_1st_f2_text=worksheet.cell_value(15,8), f2_1st_f3_text=worksheet.cell_value(15,9), f2_2nd_f1_text=worksheet.cell_value(16,7), f2_2nd_f2_text=worksheet.cell_value(16,8), f2_2nd_f3_text=worksheet.cell_value(16,9), f2_3rd_f1_text=worksheet.cell_value(17,7), f2_3rd_f2_text=worksheet.cell_value(17,8), f2_3rd_f3_text=worksheet.cell_value(17,9), f3_1st_f1_text=worksheet.cell_value(20,7), f3_1st_f2_text=worksheet.cell_value(20,8), f3_1st_f3_text=worksheet.cell_value(20,9), f3_2nd_f1_text=worksheet.cell_value(21,7), f3_2nd_f2_text=worksheet.cell_value(21,8), f3_2nd_f3_text=worksheet.cell_value(21,9), f3_3rd_f1_text=worksheet.cell_value(22,7), f3_3rd_f2_text=worksheet.cell_value(22,8), f3_3rd_f3_text=worksheet.cell_value(22,9))[0]
                            else:
                                positive_positive1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_positive1_second_level_save, f1_1st_f1_text=worksheet.cell_value(10,7), f1_1st_f2_text=worksheet.cell_value(10,8), f1_1st_f3_text=worksheet.cell_value(10,9), f1_2nd_f1_text=worksheet.cell_value(11,7), f1_2nd_f2_text=worksheet.cell_value(11,8), f1_2nd_f3_text=worksheet.cell_value(11,9), f1_3rd_f1_text=worksheet.cell_value(12,7), f1_3rd_f2_text=worksheet.cell_value(12,8), f1_3rd_f3_text=worksheet.cell_value(12,9), f2_1st_f1_text=worksheet.cell_value(15,7), f2_1st_f2_text=worksheet.cell_value(15,8), f2_1st_f3_text=worksheet.cell_value(15,9), f2_2nd_f1_text=worksheet.cell_value(16,7), f2_2nd_f2_text=worksheet.cell_value(16,8), f2_2nd_f3_text=worksheet.cell_value(16,9), f2_3rd_f1_text=worksheet.cell_value(17,7), f2_3rd_f2_text=worksheet.cell_value(17,8), f2_3rd_f3_text=worksheet.cell_value(17,9), f3_1st_f1_text=worksheet.cell_value(20,7), f3_1st_f2_text=worksheet.cell_value(20,8), f3_1st_f3_text=worksheet.cell_value(20,9), f3_2nd_f1_text=worksheet.cell_value(21,7), f3_2nd_f2_text=worksheet.cell_value(21,8), f3_2nd_f3_text=worksheet.cell_value(21,9), f3_3rd_f1_text=worksheet.cell_value(22,7), f3_3rd_f2_text=worksheet.cell_value(22,8), f3_3rd_f3_text=worksheet.cell_value(22,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Nagative Third Level values")
                        
                        try:
                            positive_positive2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_positive2_second_level_save,  f1_1st_f1_text=worksheet.cell_value(26,7), f1_1st_f2_text=worksheet.cell_value(26,8), f1_1st_f3_text=worksheet.cell_value(26,9), f1_2nd_f1_text=worksheet.cell_value(27,7), f1_2nd_f2_text=worksheet.cell_value(27,8), f1_2nd_f3_text=worksheet.cell_value(27,9), f1_3rd_f1_text=worksheet.cell_value(28,7), f1_3rd_f2_text=worksheet.cell_value(28,8), f1_3rd_f3_text=worksheet.cell_value(28,9), f2_1st_f1_text=worksheet.cell_value(31,7), f2_1st_f2_text=worksheet.cell_value(31,8), f2_1st_f3_text=worksheet.cell_value(31,9), f2_2nd_f1_text=worksheet.cell_value(32,7), f2_2nd_f2_text=worksheet.cell_value(32,8), f2_2nd_f3_text=worksheet.cell_value(32,9), f2_3rd_f1_text=worksheet.cell_value(33,7), f2_3rd_f2_text=worksheet.cell_value(33,8), f2_3rd_f3_text=worksheet.cell_value(33,9), f3_1st_f1_text=worksheet.cell_value(36,7), f3_1st_f2_text=worksheet.cell_value(36,8), f3_1st_f3_text=worksheet.cell_value(36,9), f3_2nd_f1_text=worksheet.cell_value(37,7), f3_2nd_f2_text=worksheet.cell_value(37,8), f3_2nd_f3_text=worksheet.cell_value(37,9), f3_3rd_f1_text=worksheet.cell_value(38,7), f3_3rd_f2_text=worksheet.cell_value(38,8), f3_3rd_f3_text=worksheet.cell_value(38,9))
                            if positive_positive2_third_level_check:
                                positive_positive2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_positive2_second_level_save, f1_1st_f1_text=worksheet.cell_value(26,7), f1_1st_f2_text=worksheet.cell_value(26,8), f1_1st_f3_text=worksheet.cell_value(26,9), f1_2nd_f1_text=worksheet.cell_value(27,7), f1_2nd_f2_text=worksheet.cell_value(27,8), f1_2nd_f3_text=worksheet.cell_value(27,9), f1_3rd_f1_text=worksheet.cell_value(28,7), f1_3rd_f2_text=worksheet.cell_value(28,8), f1_3rd_f3_text=worksheet.cell_value(28,9), f2_1st_f1_text=worksheet.cell_value(31,7), f2_1st_f2_text=worksheet.cell_value(31,8), f2_1st_f3_text=worksheet.cell_value(31,9), f2_2nd_f1_text=worksheet.cell_value(32,7), f2_2nd_f2_text=worksheet.cell_value(32,8), f2_2nd_f3_text=worksheet.cell_value(32,9), f2_3rd_f1_text=worksheet.cell_value(33,7), f2_3rd_f2_text=worksheet.cell_value(33,8), f2_3rd_f3_text=worksheet.cell_value(33,9), f3_1st_f1_text=worksheet.cell_value(36,7), f3_1st_f2_text=worksheet.cell_value(36,8), f3_1st_f3_text=worksheet.cell_value(36,9), f3_2nd_f1_text=worksheet.cell_value(37,7), f3_2nd_f2_text=worksheet.cell_value(37,8), f3_2nd_f3_text=worksheet.cell_value(37,9), f3_3rd_f1_text=worksheet.cell_value(38,7), f3_3rd_f2_text=worksheet.cell_value(38,8), f3_3rd_f3_text=worksheet.cell_value(38,9))[0]
                            else:
                                positive_positive2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_positive2_second_level_save, f1_1st_f1_text=worksheet.cell_value(26,7), f1_1st_f2_text=worksheet.cell_value(26,8), f1_1st_f3_text=worksheet.cell_value(26,9), f1_2nd_f1_text=worksheet.cell_value(27,7), f1_2nd_f2_text=worksheet.cell_value(27,8), f1_2nd_f3_text=worksheet.cell_value(27,9), f1_3rd_f1_text=worksheet.cell_value(28,7), f1_3rd_f2_text=worksheet.cell_value(28,8), f1_3rd_f3_text=worksheet.cell_value(28,9), f2_1st_f1_text=worksheet.cell_value(31,7), f2_1st_f2_text=worksheet.cell_value(31,8), f2_1st_f3_text=worksheet.cell_value(31,9), f2_2nd_f1_text=worksheet.cell_value(32,7), f2_2nd_f2_text=worksheet.cell_value(32,8), f2_2nd_f3_text=worksheet.cell_value(32,9), f2_3rd_f1_text=worksheet.cell_value(33,7), f2_3rd_f2_text=worksheet.cell_value(33,8), f2_3rd_f3_text=worksheet.cell_value(33,9), f3_1st_f1_text=worksheet.cell_value(36,7), f3_1st_f2_text=worksheet.cell_value(36,8), f3_1st_f3_text=worksheet.cell_value(36,9), f3_2nd_f1_text=worksheet.cell_value(37,7), f3_2nd_f2_text=worksheet.cell_value(37,8), f3_2nd_f3_text=worksheet.cell_value(37,9), f3_3rd_f1_text=worksheet.cell_value(38,7), f3_3rd_f2_text=worksheet.cell_value(38,8), f3_3rd_f3_text=worksheet.cell_value(38,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Negative Third Level values")
                        try:
                            positive_steps1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,7), f1_1st_f2_text=worksheet.cell_value(44,8), f1_1st_f3_text=worksheet.cell_value(44,9), f1_2nd_f1_text=worksheet.cell_value(45,7), f1_2nd_f2_text=worksheet.cell_value(45,8), f1_2nd_f3_text=worksheet.cell_value(45,9), f1_3rd_f1_text=worksheet.cell_value(46,7), f1_3rd_f2_text=worksheet.cell_value(46,8), f1_3rd_f3_text=worksheet.cell_value(46,9), f2_1st_f1_text=worksheet.cell_value(49,7), f2_1st_f2_text=worksheet.cell_value(49,8), f2_1st_f3_text=worksheet.cell_value(49,9), f2_2nd_f1_text=worksheet.cell_value(50,7), f2_2nd_f2_text=worksheet.cell_value(50,8), f2_2nd_f3_text=worksheet.cell_value(50,9), f2_3rd_f1_text=worksheet.cell_value(51,7), f2_3rd_f2_text=worksheet.cell_value(51,8), f2_3rd_f3_text=worksheet.cell_value(51,9), f3_1st_f1_text=worksheet.cell_value(54,7), f3_1st_f2_text=worksheet.cell_value(54,8), f3_1st_f3_text=worksheet.cell_value(54,9), f3_2nd_f1_text=worksheet.cell_value(55,7), f3_2nd_f2_text=worksheet.cell_value(55,8), f3_2nd_f3_text=worksheet.cell_value(55,9), f3_3rd_f1_text=worksheet.cell_value(56,7), f3_3rd_f2_text=worksheet.cell_value(56,8), f3_3rd_f3_text=worksheet.cell_value(56,9))
                            if positive_steps1_third_level_check:
                                positive_steps1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,7), f1_1st_f2_text=worksheet.cell_value(44,8), f1_1st_f3_text=worksheet.cell_value(44,9), f1_2nd_f1_text=worksheet.cell_value(45,7), f1_2nd_f2_text=worksheet.cell_value(45,8), f1_2nd_f3_text=worksheet.cell_value(45,9), f1_3rd_f1_text=worksheet.cell_value(46,7), f1_3rd_f2_text=worksheet.cell_value(46,8), f1_3rd_f3_text=worksheet.cell_value(46,9), f2_1st_f1_text=worksheet.cell_value(49,7), f2_1st_f2_text=worksheet.cell_value(49,8), f2_1st_f3_text=worksheet.cell_value(49,9), f2_2nd_f1_text=worksheet.cell_value(50,7), f2_2nd_f2_text=worksheet.cell_value(50,8), f2_2nd_f3_text=worksheet.cell_value(50,9), f2_3rd_f1_text=worksheet.cell_value(51,7), f2_3rd_f2_text=worksheet.cell_value(51,8), f2_3rd_f3_text=worksheet.cell_value(51,9), f3_1st_f1_text=worksheet.cell_value(54,7), f3_1st_f2_text=worksheet.cell_value(54,8), f3_1st_f3_text=worksheet.cell_value(54,9), f3_2nd_f1_text=worksheet.cell_value(55,7), f3_2nd_f2_text=worksheet.cell_value(55,8), f3_2nd_f3_text=worksheet.cell_value(55,9), f3_3rd_f1_text=worksheet.cell_value(56,7), f3_3rd_f2_text=worksheet.cell_value(56,8), f3_3rd_f3_text=worksheet.cell_value(56,9))[0]
                            else:
                                positive_steps1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,7), f1_1st_f2_text=worksheet.cell_value(44,8), f1_1st_f3_text=worksheet.cell_value(44,9), f1_2nd_f1_text=worksheet.cell_value(45,7), f1_2nd_f2_text=worksheet.cell_value(45,8), f1_2nd_f3_text=worksheet.cell_value(45,9), f1_3rd_f1_text=worksheet.cell_value(46,7), f1_3rd_f2_text=worksheet.cell_value(46,8), f1_3rd_f3_text=worksheet.cell_value(46,9), f2_1st_f1_text=worksheet.cell_value(49,7), f2_1st_f2_text=worksheet.cell_value(49,8), f2_1st_f3_text=worksheet.cell_value(49,9), f2_2nd_f1_text=worksheet.cell_value(50,7), f2_2nd_f2_text=worksheet.cell_value(50,8), f2_2nd_f3_text=worksheet.cell_value(50,9), f2_3rd_f1_text=worksheet.cell_value(51,7), f2_3rd_f2_text=worksheet.cell_value(51,8), f2_3rd_f3_text=worksheet.cell_value(51,9), f3_1st_f1_text=worksheet.cell_value(54,7), f3_1st_f2_text=worksheet.cell_value(54,8), f3_1st_f3_text=worksheet.cell_value(54,9), f3_2nd_f1_text=worksheet.cell_value(55,7), f3_2nd_f2_text=worksheet.cell_value(55,8), f3_2nd_f3_text=worksheet.cell_value(55,9), f3_3rd_f1_text=worksheet.cell_value(56,7), f3_3rd_f2_text=worksheet.cell_value(56,8), f3_3rd_f3_text=worksheet.cell_value(56,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Steps Third Level values")
                        
                        try:
                            positive_steps2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,7), f1_1st_f2_text=worksheet.cell_value(60,8), f1_1st_f3_text=worksheet.cell_value(60,9), f1_2nd_f1_text=worksheet.cell_value(61,7), f1_2nd_f2_text=worksheet.cell_value(61,8), f1_2nd_f3_text=worksheet.cell_value(61,9), f1_3rd_f1_text=worksheet.cell_value(62,7), f1_3rd_f2_text=worksheet.cell_value(62,8), f1_3rd_f3_text=worksheet.cell_value(62,9), f2_1st_f1_text=worksheet.cell_value(65,7), f2_1st_f2_text=worksheet.cell_value(65,8), f2_1st_f3_text=worksheet.cell_value(65,9), f2_2nd_f1_text=worksheet.cell_value(66,7), f2_2nd_f2_text=worksheet.cell_value(66,8), f2_2nd_f3_text=worksheet.cell_value(66,9), f2_3rd_f1_text=worksheet.cell_value(67,7), f2_3rd_f2_text=worksheet.cell_value(67,8), f2_3rd_f3_text=worksheet.cell_value(67,9), f3_1st_f1_text=worksheet.cell_value(70,7), f3_1st_f2_text=worksheet.cell_value(70,8), f3_1st_f3_text=worksheet.cell_value(70,9), f3_2nd_f1_text=worksheet.cell_value(71,7), f3_2nd_f2_text=worksheet.cell_value(71,8), f3_2nd_f3_text=worksheet.cell_value(71,9), f3_3rd_f1_text=worksheet.cell_value(72,7), f3_3rd_f2_text=worksheet.cell_value(72,8), f3_3rd_f3_text=worksheet.cell_value(72,9))
                            if positive_steps2_third_level_check:
                                positive_steps2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,7), f1_1st_f2_text=worksheet.cell_value(60,8), f1_1st_f3_text=worksheet.cell_value(60,9), f1_2nd_f1_text=worksheet.cell_value(61,7), f1_2nd_f2_text=worksheet.cell_value(61,8), f1_2nd_f3_text=worksheet.cell_value(61,9), f1_3rd_f1_text=worksheet.cell_value(62,7), f1_3rd_f2_text=worksheet.cell_value(62,8), f1_3rd_f3_text=worksheet.cell_value(62,9), f2_1st_f1_text=worksheet.cell_value(65,7), f2_1st_f2_text=worksheet.cell_value(65,8), f2_1st_f3_text=worksheet.cell_value(65,9), f2_2nd_f1_text=worksheet.cell_value(66,7), f2_2nd_f2_text=worksheet.cell_value(66,8), f2_2nd_f3_text=worksheet.cell_value(66,9), f2_3rd_f1_text=worksheet.cell_value(67,7), f2_3rd_f2_text=worksheet.cell_value(67,8), f2_3rd_f3_text=worksheet.cell_value(67,9), f3_1st_f1_text=worksheet.cell_value(70,7), f3_1st_f2_text=worksheet.cell_value(70,8), f3_1st_f3_text=worksheet.cell_value(70,9), f3_2nd_f1_text=worksheet.cell_value(71,7), f3_2nd_f2_text=worksheet.cell_value(71,8), f3_2nd_f3_text=worksheet.cell_value(71,9), f3_3rd_f1_text=worksheet.cell_value(72,7), f3_3rd_f2_text=worksheet.cell_value(72,8), f3_3rd_f3_text=worksheet.cell_value(72,9))[0]
                            else:
                                positive_steps2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,7), f1_1st_f2_text=worksheet.cell_value(60,8), f1_1st_f3_text=worksheet.cell_value(60,9), f1_2nd_f1_text=worksheet.cell_value(61,7), f1_2nd_f2_text=worksheet.cell_value(61,8), f1_2nd_f3_text=worksheet.cell_value(61,9), f1_3rd_f1_text=worksheet.cell_value(62,7), f1_3rd_f2_text=worksheet.cell_value(62,8), f1_3rd_f3_text=worksheet.cell_value(62,9), f2_1st_f1_text=worksheet.cell_value(65,7), f2_1st_f2_text=worksheet.cell_value(65,8), f2_1st_f3_text=worksheet.cell_value(65,9), f2_2nd_f1_text=worksheet.cell_value(66,7), f2_2nd_f2_text=worksheet.cell_value(66,8), f2_2nd_f3_text=worksheet.cell_value(66,9), f2_3rd_f1_text=worksheet.cell_value(67,7), f2_3rd_f2_text=worksheet.cell_value(67,8), f2_3rd_f3_text=worksheet.cell_value(67,9), f3_1st_f1_text=worksheet.cell_value(70,7), f3_1st_f2_text=worksheet.cell_value(70,8), f3_1st_f3_text=worksheet.cell_value(70,9), f3_2nd_f1_text=worksheet.cell_value(71,7), f3_2nd_f2_text=worksheet.cell_value(71,8), f3_2nd_f3_text=worksheet.cell_value(71,9), f3_3rd_f1_text=worksheet.cell_value(72,7), f3_3rd_f2_text=worksheet.cell_value(72,8), f3_3rd_f3_text=worksheet.cell_value(72,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Steps Third Level values")
                        
                        try:
                            positive_power1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_power1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,7), f1_1st_f2_text=worksheet.cell_value(78,8), f1_1st_f3_text=worksheet.cell_value(78,9), f1_2nd_f1_text=worksheet.cell_value(79,7), f1_2nd_f2_text=worksheet.cell_value(79,8), f1_2nd_f3_text=worksheet.cell_value(79,9), f1_3rd_f1_text=worksheet.cell_value(80,7), f1_3rd_f2_text=worksheet.cell_value(80,8), f1_3rd_f3_text=worksheet.cell_value(80,9), f2_1st_f1_text=worksheet.cell_value(83,7), f2_1st_f2_text=worksheet.cell_value(83,8), f2_1st_f3_text=worksheet.cell_value(83,9), f2_2nd_f1_text=worksheet.cell_value(84,7), f2_2nd_f2_text=worksheet.cell_value(84,8), f2_2nd_f3_text=worksheet.cell_value(84,9), f2_3rd_f1_text=worksheet.cell_value(85,7), f2_3rd_f2_text=worksheet.cell_value(85,8), f2_3rd_f3_text=worksheet.cell_value(85,9), f3_1st_f1_text=worksheet.cell_value(88,7), f3_1st_f2_text=worksheet.cell_value(88,8), f3_1st_f3_text=worksheet.cell_value(88,9), f3_2nd_f1_text=worksheet.cell_value(89,7), f3_2nd_f2_text=worksheet.cell_value(89,8), f3_2nd_f3_text=worksheet.cell_value(89,9), f3_3rd_f1_text=worksheet.cell_value(90,7), f3_3rd_f2_text=worksheet.cell_value(90,8), f3_3rd_f3_text=worksheet.cell_value(90,9))
                            if positive_power1_third_level_check:
                                positive_power1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_power1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,7), f1_1st_f2_text=worksheet.cell_value(78,8), f1_1st_f3_text=worksheet.cell_value(78,9), f1_2nd_f1_text=worksheet.cell_value(79,7), f1_2nd_f2_text=worksheet.cell_value(79,8), f1_2nd_f3_text=worksheet.cell_value(79,9), f1_3rd_f1_text=worksheet.cell_value(80,7), f1_3rd_f2_text=worksheet.cell_value(80,8), f1_3rd_f3_text=worksheet.cell_value(80,9), f2_1st_f1_text=worksheet.cell_value(83,7), f2_1st_f2_text=worksheet.cell_value(83,8), f2_1st_f3_text=worksheet.cell_value(83,9), f2_2nd_f1_text=worksheet.cell_value(84,7), f2_2nd_f2_text=worksheet.cell_value(84,8), f2_2nd_f3_text=worksheet.cell_value(84,9), f2_3rd_f1_text=worksheet.cell_value(85,7), f2_3rd_f2_text=worksheet.cell_value(85,8), f2_3rd_f3_text=worksheet.cell_value(85,9), f3_1st_f1_text=worksheet.cell_value(88,7), f3_1st_f2_text=worksheet.cell_value(88,8), f3_1st_f3_text=worksheet.cell_value(88,9), f3_2nd_f1_text=worksheet.cell_value(89,7), f3_2nd_f2_text=worksheet.cell_value(89,8), f3_2nd_f3_text=worksheet.cell_value(89,9), f3_3rd_f1_text=worksheet.cell_value(90,7), f3_3rd_f2_text=worksheet.cell_value(90,8), f3_3rd_f3_text=worksheet.cell_value(90,9))[0]
                            else:
                                positive_power1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_power1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,7), f1_1st_f2_text=worksheet.cell_value(78,8), f1_1st_f3_text=worksheet.cell_value(78,9), f1_2nd_f1_text=worksheet.cell_value(79,7), f1_2nd_f2_text=worksheet.cell_value(79,8), f1_2nd_f3_text=worksheet.cell_value(79,9), f1_3rd_f1_text=worksheet.cell_value(80,7), f1_3rd_f2_text=worksheet.cell_value(80,8), f1_3rd_f3_text=worksheet.cell_value(80,9), f2_1st_f1_text=worksheet.cell_value(83,7), f2_1st_f2_text=worksheet.cell_value(83,8), f2_1st_f3_text=worksheet.cell_value(83,9), f2_2nd_f1_text=worksheet.cell_value(84,7), f2_2nd_f2_text=worksheet.cell_value(84,8), f2_2nd_f3_text=worksheet.cell_value(84,9), f2_3rd_f1_text=worksheet.cell_value(85,7), f2_3rd_f2_text=worksheet.cell_value(85,8), f2_3rd_f3_text=worksheet.cell_value(85,9), f3_1st_f1_text=worksheet.cell_value(88,7), f3_1st_f2_text=worksheet.cell_value(88,8), f3_1st_f3_text=worksheet.cell_value(88,9), f3_2nd_f1_text=worksheet.cell_value(89,7), f3_2nd_f2_text=worksheet.cell_value(89,8), f3_2nd_f3_text=worksheet.cell_value(89,9), f3_3rd_f1_text=worksheet.cell_value(90,7), f3_3rd_f2_text=worksheet.cell_value(90,8), f3_3rd_f3_text=worksheet.cell_value(90,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Weak Third Level values")
                        
                        try:
                            positive_power2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_power2_second_level_save,  f1_1st_f1_text=worksheet.cell_value(94,7), f1_1st_f2_text=worksheet.cell_value(94,8), f1_1st_f3_text=worksheet.cell_value(94,9), f1_2nd_f1_text=worksheet.cell_value(95,7), f1_2nd_f2_text=worksheet.cell_value(95,8), f1_2nd_f3_text=worksheet.cell_value(95,9), f1_3rd_f1_text=worksheet.cell_value(96,7), f1_3rd_f2_text=worksheet.cell_value(96,8), f1_3rd_f3_text=worksheet.cell_value(96,9), f2_1st_f1_text=worksheet.cell_value(99,7), f2_1st_f2_text=worksheet.cell_value(99,8), f2_1st_f3_text=worksheet.cell_value(99,9), f2_2nd_f1_text=worksheet.cell_value(100,7), f2_2nd_f2_text=worksheet.cell_value(100,8), f2_2nd_f3_text=worksheet.cell_value(100,9), f2_3rd_f1_text=worksheet.cell_value(101,7), f2_3rd_f2_text=worksheet.cell_value(101,8), f2_3rd_f3_text=worksheet.cell_value(101,9), f3_1st_f1_text=worksheet.cell_value(104,7), f3_1st_f2_text=worksheet.cell_value(104,8), f3_1st_f3_text=worksheet.cell_value(104,9), f3_2nd_f1_text=worksheet.cell_value(105,7), f3_2nd_f2_text=worksheet.cell_value(105,8), f3_2nd_f3_text=worksheet.cell_value(105,9), f3_3rd_f1_text=worksheet.cell_value(106,7), f3_3rd_f2_text=worksheet.cell_value(106,8), f3_3rd_f3_text=worksheet.cell_value(106,9))
                            if positive_power2_third_level_check:
                                positive_power2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_power2_second_level_save, f1_1st_f1_text=worksheet.cell_value(94,7), f1_1st_f2_text=worksheet.cell_value(94,8), f1_1st_f3_text=worksheet.cell_value(94,9), f1_2nd_f1_text=worksheet.cell_value(95,7), f1_2nd_f2_text=worksheet.cell_value(95,8), f1_2nd_f3_text=worksheet.cell_value(95,9), f1_3rd_f1_text=worksheet.cell_value(96,7), f1_3rd_f2_text=worksheet.cell_value(96,8), f1_3rd_f3_text=worksheet.cell_value(96,9), f2_1st_f1_text=worksheet.cell_value(99,7), f2_1st_f2_text=worksheet.cell_value(99,8), f2_1st_f3_text=worksheet.cell_value(99,9), f2_2nd_f1_text=worksheet.cell_value(100,7), f2_2nd_f2_text=worksheet.cell_value(100,8), f2_2nd_f3_text=worksheet.cell_value(100,9), f2_3rd_f1_text=worksheet.cell_value(101,7), f2_3rd_f2_text=worksheet.cell_value(101,8), f2_3rd_f3_text=worksheet.cell_value(101,9), f3_1st_f1_text=worksheet.cell_value(104,7), f3_1st_f2_text=worksheet.cell_value(104,8), f3_1st_f3_text=worksheet.cell_value(104,9), f3_2nd_f1_text=worksheet.cell_value(105,7), f3_2nd_f2_text=worksheet.cell_value(105,8), f3_2nd_f3_text=worksheet.cell_value(105,9), f3_3rd_f1_text=worksheet.cell_value(106,7), f3_3rd_f2_text=worksheet.cell_value(106,8), f3_3rd_f3_text=worksheet.cell_value(106,9))[0]
                            else:
                                positive_power2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_power2_second_level_save, f1_1st_f1_text=worksheet.cell_value(94,7), f1_1st_f2_text=worksheet.cell_value(94,8), f1_1st_f3_text=worksheet.cell_value(94,9), f1_2nd_f1_text=worksheet.cell_value(95,7), f1_2nd_f2_text=worksheet.cell_value(95,8), f1_2nd_f3_text=worksheet.cell_value(95,9), f1_3rd_f1_text=worksheet.cell_value(96,7), f1_3rd_f2_text=worksheet.cell_value(96,8), f1_3rd_f3_text=worksheet.cell_value(96,9), f2_1st_f1_text=worksheet.cell_value(99,7), f2_1st_f2_text=worksheet.cell_value(99,8), f2_1st_f3_text=worksheet.cell_value(99,9), f2_2nd_f1_text=worksheet.cell_value(100,7), f2_2nd_f2_text=worksheet.cell_value(100,8), f2_2nd_f3_text=worksheet.cell_value(100,9), f2_3rd_f1_text=worksheet.cell_value(101,7), f2_3rd_f2_text=worksheet.cell_value(101,8), f2_3rd_f3_text=worksheet.cell_value(101,9), f3_1st_f1_text=worksheet.cell_value(104,7), f3_1st_f2_text=worksheet.cell_value(104,8), f3_1st_f3_text=worksheet.cell_value(104,9), f3_2nd_f1_text=worksheet.cell_value(105,7), f3_2nd_f2_text=worksheet.cell_value(105,8), f3_2nd_f3_text=worksheet.cell_value(105,9), f3_3rd_f1_text=worksheet.cell_value(106,7), f3_3rd_f2_text=worksheet.cell_value(106,8), f3_3rd_f3_text=worksheet.cell_value(106,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Weak Third Level values")
                        
                        try:
                            positive_high1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_high1_second_level_save,  f1_1st_f1_text=worksheet.cell_value(112,7), f1_1st_f2_text=worksheet.cell_value(112,8), f1_1st_f3_text=worksheet.cell_value(112,9), f1_2nd_f1_text=worksheet.cell_value(113,7), f1_2nd_f2_text=worksheet.cell_value(113,8), f1_2nd_f3_text=worksheet.cell_value(113,9), f1_3rd_f1_text=worksheet.cell_value(114,7), f1_3rd_f2_text=worksheet.cell_value(114,8), f1_3rd_f3_text=worksheet.cell_value(114,9), f2_1st_f1_text=worksheet.cell_value(117,7), f2_1st_f2_text=worksheet.cell_value(117,8), f2_1st_f3_text=worksheet.cell_value(117,9), f2_2nd_f1_text=worksheet.cell_value(118,7), f2_2nd_f2_text=worksheet.cell_value(118,8), f2_2nd_f3_text=worksheet.cell_value(118,9), f2_3rd_f1_text=worksheet.cell_value(119,7), f2_3rd_f2_text=worksheet.cell_value(119,8), f2_3rd_f3_text=worksheet.cell_value(119,9), f3_1st_f1_text=worksheet.cell_value(122,7), f3_1st_f2_text=worksheet.cell_value(122,8), f3_1st_f3_text=worksheet.cell_value(122,9), f3_2nd_f1_text=worksheet.cell_value(123,7), f3_2nd_f2_text=worksheet.cell_value(123,8), f3_2nd_f3_text=worksheet.cell_value(123,9), f3_3rd_f1_text=worksheet.cell_value(124,7), f3_3rd_f2_text=worksheet.cell_value(124,8), f3_3rd_f3_text=worksheet.cell_value(124,9))
                            if positive_high1_third_level_check:
                                positive_high1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_high1_second_level_save, f1_1st_f1_text=worksheet.cell_value(112,7), f1_1st_f2_text=worksheet.cell_value(112,8), f1_1st_f3_text=worksheet.cell_value(112,9), f1_2nd_f1_text=worksheet.cell_value(113,7), f1_2nd_f2_text=worksheet.cell_value(113,8), f1_2nd_f3_text=worksheet.cell_value(113,9), f1_3rd_f1_text=worksheet.cell_value(114,7), f1_3rd_f2_text=worksheet.cell_value(114,8), f1_3rd_f3_text=worksheet.cell_value(114,9), f2_1st_f1_text=worksheet.cell_value(117,7), f2_1st_f2_text=worksheet.cell_value(117,8), f2_1st_f3_text=worksheet.cell_value(117,9), f2_2nd_f1_text=worksheet.cell_value(118,7), f2_2nd_f2_text=worksheet.cell_value(118,8), f2_2nd_f3_text=worksheet.cell_value(118,9), f2_3rd_f1_text=worksheet.cell_value(119,7), f2_3rd_f2_text=worksheet.cell_value(119,8), f2_3rd_f3_text=worksheet.cell_value(119,9), f3_1st_f1_text=worksheet.cell_value(122,7), f3_1st_f2_text=worksheet.cell_value(122,8), f3_1st_f3_text=worksheet.cell_value(122,9), f3_2nd_f1_text=worksheet.cell_value(123,7), f3_2nd_f2_text=worksheet.cell_value(123,8), f3_2nd_f3_text=worksheet.cell_value(123,9), f3_3rd_f1_text=worksheet.cell_value(124,7), f3_3rd_f2_text=worksheet.cell_value(124,8), f3_3rd_f3_text=worksheet.cell_value(124,9))[0]
                            else:
                                positive_high1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_high1_second_level_save, f1_1st_f1_text=worksheet.cell_value(112,7), f1_1st_f2_text=worksheet.cell_value(112,8), f1_1st_f3_text=worksheet.cell_value(112,9), f1_2nd_f1_text=worksheet.cell_value(113,7), f1_2nd_f2_text=worksheet.cell_value(113,8), f1_2nd_f3_text=worksheet.cell_value(113,9), f1_3rd_f1_text=worksheet.cell_value(114,7), f1_3rd_f2_text=worksheet.cell_value(114,8), f1_3rd_f3_text=worksheet.cell_value(114,9), f2_1st_f1_text=worksheet.cell_value(117,7), f2_1st_f2_text=worksheet.cell_value(117,8), f2_1st_f3_text=worksheet.cell_value(117,9), f2_2nd_f1_text=worksheet.cell_value(118,7), f2_2nd_f2_text=worksheet.cell_value(118,8), f2_2nd_f3_text=worksheet.cell_value(118,9), f2_3rd_f1_text=worksheet.cell_value(119,7), f2_3rd_f2_text=worksheet.cell_value(119,8), f2_3rd_f3_text=worksheet.cell_value(119,9), f3_1st_f1_text=worksheet.cell_value(122,7), f3_1st_f2_text=worksheet.cell_value(122,8), f3_1st_f3_text=worksheet.cell_value(122,9), f3_2nd_f1_text=worksheet.cell_value(123,7), f3_2nd_f2_text=worksheet.cell_value(123,8), f3_2nd_f3_text=worksheet.cell_value(123,9), f3_3rd_f1_text=worksheet.cell_value(124,7), f3_3rd_f2_text=worksheet.cell_value(124,8), f3_3rd_f3_text=worksheet.cell_value(124,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Low Third Level values")
                        
                        try:
                            positive_high2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_high2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,7), f1_1st_f2_text=worksheet.cell_value(128,8), f1_1st_f3_text=worksheet.cell_value(128,9), f1_2nd_f1_text=worksheet.cell_value(129,7), f1_2nd_f2_text=worksheet.cell_value(129,8), f1_2nd_f3_text=worksheet.cell_value(129,9), f1_3rd_f1_text=worksheet.cell_value(130,7), f1_3rd_f2_text=worksheet.cell_value(130,8), f1_3rd_f3_text=worksheet.cell_value(130,9), f2_1st_f1_text=worksheet.cell_value(133,7), f2_1st_f2_text=worksheet.cell_value(133,8), f2_1st_f3_text=worksheet.cell_value(133,9), f2_2nd_f1_text=worksheet.cell_value(134,7), f2_2nd_f2_text=worksheet.cell_value(134,8), f2_2nd_f3_text=worksheet.cell_value(134,9), f2_3rd_f1_text=worksheet.cell_value(135,7), f2_3rd_f2_text=worksheet.cell_value(135,8), f2_3rd_f3_text=worksheet.cell_value(135,9), f3_1st_f1_text=worksheet.cell_value(138,7), f3_1st_f2_text=worksheet.cell_value(138,8), f3_1st_f3_text=worksheet.cell_value(138,9), f3_2nd_f1_text=worksheet.cell_value(139,7), f3_2nd_f2_text=worksheet.cell_value(139,8), f3_2nd_f3_text=worksheet.cell_value(139,9), f3_3rd_f1_text=worksheet.cell_value(140,7), f3_3rd_f2_text=worksheet.cell_value(140,8), f3_3rd_f3_text=worksheet.cell_value(140,9))
                            if positive_high2_third_level_check:
                                positive_high2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_high2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,7), f1_1st_f2_text=worksheet.cell_value(128,8), f1_1st_f3_text=worksheet.cell_value(128,9), f1_2nd_f1_text=worksheet.cell_value(129,7), f1_2nd_f2_text=worksheet.cell_value(129,8), f1_2nd_f3_text=worksheet.cell_value(129,9), f1_3rd_f1_text=worksheet.cell_value(130,7), f1_3rd_f2_text=worksheet.cell_value(130,8), f1_3rd_f3_text=worksheet.cell_value(130,9), f2_1st_f1_text=worksheet.cell_value(133,7), f2_1st_f2_text=worksheet.cell_value(133,8), f2_1st_f3_text=worksheet.cell_value(133,9), f2_2nd_f1_text=worksheet.cell_value(134,7), f2_2nd_f2_text=worksheet.cell_value(134,8), f2_2nd_f3_text=worksheet.cell_value(134,9), f2_3rd_f1_text=worksheet.cell_value(135,7), f2_3rd_f2_text=worksheet.cell_value(135,8), f2_3rd_f3_text=worksheet.cell_value(135,9), f3_1st_f1_text=worksheet.cell_value(138,7), f3_1st_f2_text=worksheet.cell_value(138,8), f3_1st_f3_text=worksheet.cell_value(138,9), f3_2nd_f1_text=worksheet.cell_value(139,7), f3_2nd_f2_text=worksheet.cell_value(139,8), f3_2nd_f3_text=worksheet.cell_value(139,9), f3_3rd_f1_text=worksheet.cell_value(140,7), f3_3rd_f2_text=worksheet.cell_value(140,8), f3_3rd_f3_text=worksheet.cell_value(140,9))[0]
                            else:
                                positive_high2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_high2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,7), f1_1st_f2_text=worksheet.cell_value(128,8), f1_1st_f3_text=worksheet.cell_value(128,9), f1_2nd_f1_text=worksheet.cell_value(129,7), f1_2nd_f2_text=worksheet.cell_value(129,8), f1_2nd_f3_text=worksheet.cell_value(129,9), f1_3rd_f1_text=worksheet.cell_value(130,7), f1_3rd_f2_text=worksheet.cell_value(130,8), f1_3rd_f3_text=worksheet.cell_value(130,9), f2_1st_f1_text=worksheet.cell_value(133,7), f2_1st_f2_text=worksheet.cell_value(133,8), f2_1st_f3_text=worksheet.cell_value(133,9), f2_2nd_f1_text=worksheet.cell_value(134,7), f2_2nd_f2_text=worksheet.cell_value(134,8), f2_2nd_f3_text=worksheet.cell_value(134,9), f2_3rd_f1_text=worksheet.cell_value(135,7), f2_3rd_f2_text=worksheet.cell_value(135,8), f2_3rd_f3_text=worksheet.cell_value(135,9), f3_1st_f1_text=worksheet.cell_value(138,7), f3_1st_f2_text=worksheet.cell_value(138,8), f3_1st_f3_text=worksheet.cell_value(138,9), f3_2nd_f1_text=worksheet.cell_value(139,7), f3_2nd_f2_text=worksheet.cell_value(139,8), f3_2nd_f3_text=worksheet.cell_value(139,9), f3_3rd_f1_text=worksheet.cell_value(140,7), f3_3rd_f2_text=worksheet.cell_value(140,8), f3_3rd_f3_text=worksheet.cell_value(140,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Low Third Level values")
                        
                        try:
                            positive_current1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_current1_second_level_save,  f1_1st_f1_text=worksheet.cell_value(146,7), f1_1st_f2_text=worksheet.cell_value(146,8), f1_1st_f3_text=worksheet.cell_value(146,9), f1_2nd_f1_text=worksheet.cell_value(147,7), f1_2nd_f2_text=worksheet.cell_value(147,8), f1_2nd_f3_text=worksheet.cell_value(147,9), f1_3rd_f1_text=worksheet.cell_value(148,7), f1_3rd_f2_text=worksheet.cell_value(148,8), f1_3rd_f3_text=worksheet.cell_value(148,9), f2_1st_f1_text=worksheet.cell_value(151,7), f2_1st_f2_text=worksheet.cell_value(151,8), f2_1st_f3_text=worksheet.cell_value(151,9), f2_2nd_f1_text=worksheet.cell_value(152,7), f2_2nd_f2_text=worksheet.cell_value(152,8), f2_2nd_f3_text=worksheet.cell_value(152,9), f2_3rd_f1_text=worksheet.cell_value(153,7), f2_3rd_f2_text=worksheet.cell_value(153,8), f2_3rd_f3_text=worksheet.cell_value(153,9), f3_1st_f1_text=worksheet.cell_value(156,7), f3_1st_f2_text=worksheet.cell_value(156,8), f3_1st_f3_text=worksheet.cell_value(156,9), f3_2nd_f1_text=worksheet.cell_value(157,7), f3_2nd_f2_text=worksheet.cell_value(157,8), f3_2nd_f3_text=worksheet.cell_value(157,9), f3_3rd_f1_text=worksheet.cell_value(158,7), f3_3rd_f2_text=worksheet.cell_value(158,8), f3_3rd_f3_text=worksheet.cell_value(158,9))
                            if positive_current1_third_level_check:
                                positive_current1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_current1_second_level_save, f1_1st_f1_text=worksheet.cell_value(146,7), f1_1st_f2_text=worksheet.cell_value(146,8), f1_1st_f3_text=worksheet.cell_value(146,9), f1_2nd_f1_text=worksheet.cell_value(147,7), f1_2nd_f2_text=worksheet.cell_value(147,8), f1_2nd_f3_text=worksheet.cell_value(147,9), f1_3rd_f1_text=worksheet.cell_value(148,7), f1_3rd_f2_text=worksheet.cell_value(148,8), f1_3rd_f3_text=worksheet.cell_value(148,9), f2_1st_f1_text=worksheet.cell_value(151,7), f2_1st_f2_text=worksheet.cell_value(151,8), f2_1st_f3_text=worksheet.cell_value(151,9), f2_2nd_f1_text=worksheet.cell_value(152,7), f2_2nd_f2_text=worksheet.cell_value(152,8), f2_2nd_f3_text=worksheet.cell_value(152,9), f2_3rd_f1_text=worksheet.cell_value(153,7), f2_3rd_f2_text=worksheet.cell_value(153,8), f2_3rd_f3_text=worksheet.cell_value(153,9), f3_1st_f1_text=worksheet.cell_value(156,7), f3_1st_f2_text=worksheet.cell_value(156,8), f3_1st_f3_text=worksheet.cell_value(156,9), f3_2nd_f1_text=worksheet.cell_value(157,7), f3_2nd_f2_text=worksheet.cell_value(157,8), f3_2nd_f3_text=worksheet.cell_value(157,9), f3_3rd_f1_text=worksheet.cell_value(158,7), f3_3rd_f2_text=worksheet.cell_value(158,8), f3_3rd_f3_text=worksheet.cell_value(158,9))[0]
                            else:
                                positive_current1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_current1_second_level_save, f1_1st_f1_text=worksheet.cell_value(146,7), f1_1st_f2_text=worksheet.cell_value(146,8), f1_1st_f3_text=worksheet.cell_value(146,9), f1_2nd_f1_text=worksheet.cell_value(147,7), f1_2nd_f2_text=worksheet.cell_value(147,8), f1_2nd_f3_text=worksheet.cell_value(147,9), f1_3rd_f1_text=worksheet.cell_value(148,7), f1_3rd_f2_text=worksheet.cell_value(148,8), f1_3rd_f3_text=worksheet.cell_value(148,9), f2_1st_f1_text=worksheet.cell_value(151,7), f2_1st_f2_text=worksheet.cell_value(151,8), f2_1st_f3_text=worksheet.cell_value(151,9), f2_2nd_f1_text=worksheet.cell_value(152,7), f2_2nd_f2_text=worksheet.cell_value(152,8), f2_2nd_f3_text=worksheet.cell_value(152,9), f2_3rd_f1_text=worksheet.cell_value(153,7), f2_3rd_f2_text=worksheet.cell_value(153,8), f2_3rd_f3_text=worksheet.cell_value(153,9), f3_1st_f1_text=worksheet.cell_value(156,7), f3_1st_f2_text=worksheet.cell_value(156,8), f3_1st_f3_text=worksheet.cell_value(156,9), f3_2nd_f1_text=worksheet.cell_value(157,7), f3_2nd_f2_text=worksheet.cell_value(157,8), f3_2nd_f3_text=worksheet.cell_value(157,9), f3_3rd_f1_text=worksheet.cell_value(158,7), f3_3rd_f2_text=worksheet.cell_value(158,8), f3_3rd_f3_text=worksheet.cell_value(158,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Current Third Level values")
                        
                        try:
                            positive_current2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,7), f1_1st_f2_text=worksheet.cell_value(162,8), f1_1st_f3_text=worksheet.cell_value(162,9), f1_2nd_f1_text=worksheet.cell_value(163,7), f1_2nd_f2_text=worksheet.cell_value(163,8), f1_2nd_f3_text=worksheet.cell_value(163,9), f1_3rd_f1_text=worksheet.cell_value(164,7), f1_3rd_f2_text=worksheet.cell_value(164,8), f1_3rd_f3_text=worksheet.cell_value(164,9), f2_1st_f1_text=worksheet.cell_value(167,7), f2_1st_f2_text=worksheet.cell_value(167,8), f2_1st_f3_text=worksheet.cell_value(167,9), f2_2nd_f1_text=worksheet.cell_value(168,7), f2_2nd_f2_text=worksheet.cell_value(168,8), f2_2nd_f3_text=worksheet.cell_value(168,9), f2_3rd_f1_text=worksheet.cell_value(169,7), f2_3rd_f2_text=worksheet.cell_value(169,8), f2_3rd_f3_text=worksheet.cell_value(169,9), f3_1st_f1_text=worksheet.cell_value(172,7), f3_1st_f2_text=worksheet.cell_value(172,8), f3_1st_f3_text=worksheet.cell_value(172,9), f3_2nd_f1_text=worksheet.cell_value(173,7), f3_2nd_f2_text=worksheet.cell_value(173,8), f3_2nd_f3_text=worksheet.cell_value(173,9), f3_3rd_f1_text=worksheet.cell_value(174,7), f3_3rd_f2_text=worksheet.cell_value(174,8), f3_3rd_f3_text=worksheet.cell_value(174,9))
                            if positive_current2_third_level_check:
                                positive_current2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,7), f1_1st_f2_text=worksheet.cell_value(162,8), f1_1st_f3_text=worksheet.cell_value(162,9), f1_2nd_f1_text=worksheet.cell_value(163,7), f1_2nd_f2_text=worksheet.cell_value(163,8), f1_2nd_f3_text=worksheet.cell_value(163,9), f1_3rd_f1_text=worksheet.cell_value(164,7), f1_3rd_f2_text=worksheet.cell_value(164,8), f1_3rd_f3_text=worksheet.cell_value(164,9), f2_1st_f1_text=worksheet.cell_value(167,7), f2_1st_f2_text=worksheet.cell_value(167,8), f2_1st_f3_text=worksheet.cell_value(167,9), f2_2nd_f1_text=worksheet.cell_value(168,7), f2_2nd_f2_text=worksheet.cell_value(168,8), f2_2nd_f3_text=worksheet.cell_value(168,9), f2_3rd_f1_text=worksheet.cell_value(169,7), f2_3rd_f2_text=worksheet.cell_value(169,8), f2_3rd_f3_text=worksheet.cell_value(169,9), f3_1st_f1_text=worksheet.cell_value(172,7), f3_1st_f2_text=worksheet.cell_value(172,8), f3_1st_f3_text=worksheet.cell_value(172,9), f3_2nd_f1_text=worksheet.cell_value(173,7), f3_2nd_f2_text=worksheet.cell_value(173,8), f3_2nd_f3_text=worksheet.cell_value(173,9), f3_3rd_f1_text=worksheet.cell_value(174,7), f3_3rd_f2_text=worksheet.cell_value(174,8), f3_3rd_f3_text=worksheet.cell_value(174,9))[0]
                            else:
                                positive_current2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,7), f1_1st_f2_text=worksheet.cell_value(162,8), f1_1st_f3_text=worksheet.cell_value(162,9), f1_2nd_f1_text=worksheet.cell_value(163,7), f1_2nd_f2_text=worksheet.cell_value(163,8), f1_2nd_f3_text=worksheet.cell_value(163,9), f1_3rd_f1_text=worksheet.cell_value(164,7), f1_3rd_f2_text=worksheet.cell_value(164,8), f1_3rd_f3_text=worksheet.cell_value(164,9), f2_1st_f1_text=worksheet.cell_value(167,7), f2_1st_f2_text=worksheet.cell_value(167,8), f2_1st_f3_text=worksheet.cell_value(167,9), f2_2nd_f1_text=worksheet.cell_value(168,7), f2_2nd_f2_text=worksheet.cell_value(168,8), f2_2nd_f3_text=worksheet.cell_value(168,9), f2_3rd_f1_text=worksheet.cell_value(169,7), f2_3rd_f2_text=worksheet.cell_value(169,8), f2_3rd_f3_text=worksheet.cell_value(169,9), f3_1st_f1_text=worksheet.cell_value(172,7), f3_1st_f2_text=worksheet.cell_value(172,8), f3_1st_f3_text=worksheet.cell_value(172,9), f3_2nd_f1_text=worksheet.cell_value(173,7), f3_2nd_f2_text=worksheet.cell_value(173,8), f3_2nd_f3_text=worksheet.cell_value(173,9), f3_3rd_f1_text=worksheet.cell_value(174,7), f3_3rd_f2_text=worksheet.cell_value(174,8), f3_3rd_f3_text=worksheet.cell_value(174,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Current Third Level values")
                        
                        try:
                            positive_habitats1_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,7), f1_1st_f2_text=worksheet.cell_value(180,8), f1_1st_f3_text=worksheet.cell_value(180,9), f1_2nd_f1_text=worksheet.cell_value(181,7), f1_2nd_f2_text=worksheet.cell_value(181,8), f1_2nd_f3_text=worksheet.cell_value(181,9), f1_3rd_f1_text=worksheet.cell_value(182,7), f1_3rd_f2_text=worksheet.cell_value(182,8), f1_3rd_f3_text=worksheet.cell_value(182,9), f2_1st_f1_text=worksheet.cell_value(185,7), f2_1st_f2_text=worksheet.cell_value(185,8), f2_1st_f3_text=worksheet.cell_value(185,9), f2_2nd_f1_text=worksheet.cell_value(186,7), f2_2nd_f2_text=worksheet.cell_value(186,8), f2_2nd_f3_text=worksheet.cell_value(186,9), f2_3rd_f1_text=worksheet.cell_value(187,7), f2_3rd_f2_text=worksheet.cell_value(187,8), f2_3rd_f3_text=worksheet.cell_value(187,9), f3_1st_f1_text=worksheet.cell_value(190,7), f3_1st_f2_text=worksheet.cell_value(190,8), f3_1st_f3_text=worksheet.cell_value(190,9), f3_2nd_f1_text=worksheet.cell_value(191,7), f3_2nd_f2_text=worksheet.cell_value(191,8), f3_2nd_f3_text=worksheet.cell_value(191,9), f3_3rd_f1_text=worksheet.cell_value(192,7), f3_3rd_f2_text=worksheet.cell_value(192,8), f3_3rd_f3_text=worksheet.cell_value(192,9))
                            if positive_habitats1_third_level_check:
                                positive_habitats1_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,7), f1_1st_f2_text=worksheet.cell_value(180,8), f1_1st_f3_text=worksheet.cell_value(180,9), f1_2nd_f1_text=worksheet.cell_value(181,7), f1_2nd_f2_text=worksheet.cell_value(181,8), f1_2nd_f3_text=worksheet.cell_value(181,9), f1_3rd_f1_text=worksheet.cell_value(182,7), f1_3rd_f2_text=worksheet.cell_value(182,8), f1_3rd_f3_text=worksheet.cell_value(182,9), f2_1st_f1_text=worksheet.cell_value(185,7), f2_1st_f2_text=worksheet.cell_value(185,8), f2_1st_f3_text=worksheet.cell_value(185,9), f2_2nd_f1_text=worksheet.cell_value(186,7), f2_2nd_f2_text=worksheet.cell_value(186,8), f2_2nd_f3_text=worksheet.cell_value(186,9), f2_3rd_f1_text=worksheet.cell_value(187,7), f2_3rd_f2_text=worksheet.cell_value(187,8), f2_3rd_f3_text=worksheet.cell_value(187,9), f3_1st_f1_text=worksheet.cell_value(190,7), f3_1st_f2_text=worksheet.cell_value(190,8), f3_1st_f3_text=worksheet.cell_value(190,9), f3_2nd_f1_text=worksheet.cell_value(191,7), f3_2nd_f2_text=worksheet.cell_value(191,8), f3_2nd_f3_text=worksheet.cell_value(191,9), f3_3rd_f1_text=worksheet.cell_value(192,7), f3_3rd_f2_text=worksheet.cell_value(192,8), f3_3rd_f3_text=worksheet.cell_value(192,9))[0]
                            else:
                                positive_habitats1_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,7), f1_1st_f2_text=worksheet.cell_value(180,8), f1_1st_f3_text=worksheet.cell_value(180,9), f1_2nd_f1_text=worksheet.cell_value(181,7), f1_2nd_f2_text=worksheet.cell_value(181,8), f1_2nd_f3_text=worksheet.cell_value(181,9), f1_3rd_f1_text=worksheet.cell_value(182,7), f1_3rd_f2_text=worksheet.cell_value(182,8), f1_3rd_f3_text=worksheet.cell_value(182,9), f2_1st_f1_text=worksheet.cell_value(185,7), f2_1st_f2_text=worksheet.cell_value(185,8), f2_1st_f3_text=worksheet.cell_value(185,9), f2_2nd_f1_text=worksheet.cell_value(186,7), f2_2nd_f2_text=worksheet.cell_value(186,8), f2_2nd_f3_text=worksheet.cell_value(186,9), f2_3rd_f1_text=worksheet.cell_value(187,7), f2_3rd_f2_text=worksheet.cell_value(187,8), f2_3rd_f3_text=worksheet.cell_value(187,9), f3_1st_f1_text=worksheet.cell_value(190,7), f3_1st_f2_text=worksheet.cell_value(190,8), f3_1st_f3_text=worksheet.cell_value(190,9), f3_2nd_f1_text=worksheet.cell_value(191,7), f3_2nd_f2_text=worksheet.cell_value(191,8), f3_2nd_f3_text=worksheet.cell_value(191,9), f3_3rd_f1_text=worksheet.cell_value(192,7), f3_3rd_f2_text=worksheet.cell_value(192,8), f3_3rd_f3_text=worksheet.cell_value(192,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" First Habitats Third Level values")
                        try:
                            positive_habitats2_third_level_check =PositiveThirdLevelContent.objects.filter(second_level=positive_habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,7), f1_1st_f2_text=worksheet.cell_value(196,8), f1_1st_f3_text=worksheet.cell_value(196,9), f1_2nd_f1_text=worksheet.cell_value(197,7), f1_2nd_f2_text=worksheet.cell_value(197,8), f1_2nd_f3_text=worksheet.cell_value(197,9), f1_3rd_f1_text=worksheet.cell_value(198,7), f1_3rd_f2_text=worksheet.cell_value(198,8), f1_3rd_f3_text=worksheet.cell_value(198,9), f2_1st_f1_text=worksheet.cell_value(201,7), f2_1st_f2_text=worksheet.cell_value(201,8), f2_1st_f3_text=worksheet.cell_value(201,9), f2_2nd_f1_text=worksheet.cell_value(202,7), f2_2nd_f2_text=worksheet.cell_value(202,8), f2_2nd_f3_text=worksheet.cell_value(202,9), f2_3rd_f1_text=worksheet.cell_value(203,7), f2_3rd_f2_text=worksheet.cell_value(203,8), f2_3rd_f3_text=worksheet.cell_value(203,9), f3_1st_f1_text=worksheet.cell_value(206,7), f3_1st_f2_text=worksheet.cell_value(206,8), f3_1st_f3_text=worksheet.cell_value(206,9), f3_2nd_f1_text=worksheet.cell_value(207,7), f3_2nd_f2_text=worksheet.cell_value(207,8), f3_2nd_f3_text=worksheet.cell_value(207,9), f3_3rd_f1_text=worksheet.cell_value(208,7), f3_3rd_f2_text=worksheet.cell_value(208,8), f3_3rd_f3_text=worksheet.cell_value(208,9))
                            if positive_habitats2_third_level_check:
                                positive_habitats2_third_level_save =PositiveThirdLevelContent.objects.filter(second_level=positive_habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,7), f1_1st_f2_text=worksheet.cell_value(196,8), f1_1st_f3_text=worksheet.cell_value(196,9), f1_2nd_f1_text=worksheet.cell_value(197,7), f1_2nd_f2_text=worksheet.cell_value(197,8), f1_2nd_f3_text=worksheet.cell_value(197,9), f1_3rd_f1_text=worksheet.cell_value(198,7), f1_3rd_f2_text=worksheet.cell_value(198,8), f1_3rd_f3_text=worksheet.cell_value(198,9), f2_1st_f1_text=worksheet.cell_value(201,7), f2_1st_f2_text=worksheet.cell_value(201,8), f2_1st_f3_text=worksheet.cell_value(201,9), f2_2nd_f1_text=worksheet.cell_value(202,7), f2_2nd_f2_text=worksheet.cell_value(202,8), f2_2nd_f3_text=worksheet.cell_value(202,9), f2_3rd_f1_text=worksheet.cell_value(203,7), f2_3rd_f2_text=worksheet.cell_value(203,8), f2_3rd_f3_text=worksheet.cell_value(203,9), f3_1st_f1_text=worksheet.cell_value(206,7), f3_1st_f2_text=worksheet.cell_value(206,8), f3_1st_f3_text=worksheet.cell_value(206,9), f3_2nd_f1_text=worksheet.cell_value(207,7), f3_2nd_f2_text=worksheet.cell_value(207,8), f3_2nd_f3_text=worksheet.cell_value(207,9), f3_3rd_f1_text=worksheet.cell_value(208,7), f3_3rd_f2_text=worksheet.cell_value(208,8), f3_3rd_f3_text=worksheet.cell_value(208,9))[0]
                            else:
                                positive_habitats2_third_level_save =PositiveThirdLevelContent.objects.create(second_level=positive_habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,7), f1_1st_f2_text=worksheet.cell_value(196,8), f1_1st_f3_text=worksheet.cell_value(196,9), f1_2nd_f1_text=worksheet.cell_value(197,7), f1_2nd_f2_text=worksheet.cell_value(197,8), f1_2nd_f3_text=worksheet.cell_value(197,9), f1_3rd_f1_text=worksheet.cell_value(198,7), f1_3rd_f2_text=worksheet.cell_value(198,8), f1_3rd_f3_text=worksheet.cell_value(198,9), f2_1st_f1_text=worksheet.cell_value(201,7), f2_1st_f2_text=worksheet.cell_value(201,8), f2_1st_f3_text=worksheet.cell_value(201,9), f2_2nd_f1_text=worksheet.cell_value(202,7), f2_2nd_f2_text=worksheet.cell_value(202,8), f2_2nd_f3_text=worksheet.cell_value(202,9), f2_3rd_f1_text=worksheet.cell_value(203,7), f2_3rd_f2_text=worksheet.cell_value(203,8), f2_3rd_f3_text=worksheet.cell_value(203,9), f3_1st_f1_text=worksheet.cell_value(206,7), f3_1st_f2_text=worksheet.cell_value(206,8), f3_1st_f3_text=worksheet.cell_value(206,9), f3_2nd_f1_text=worksheet.cell_value(207,7), f3_2nd_f2_text=worksheet.cell_value(207,8), f3_2nd_f3_text=worksheet.cell_value(207,9), f3_3rd_f1_text=worksheet.cell_value(208,7), f3_3rd_f2_text=worksheet.cell_value(208,8), f3_3rd_f3_text=worksheet.cell_value(208,9))
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" Second Habitats Third Level values")
                        
                        try:
                            want_check = Want.objects.filter(name=worksheet.cell_value(2,6), category=category_save, subcategory=sub_category_save, positive_i_want_show_more_content_1= positive_positive1_first_level_save,  positive_i_want_show_more_content_2= positive_positive2_first_level_save, steps_to_turn_positive_show_more_content_1= positive_steps1_first_level_save, steps_to_turn_positive_show_more_content_2=  positive_steps2_first_level_save, power_and_grace_show_more_content_1= positive_power1_first_level_save , power_and_grace_show_more_content_2= positive_power2_first_level_save, high_performance_ability_show_more_content_1= positive_high1_first_level_save, high_performance_ability_show_more_content_2= positive_high2_first_level_save, current_habits_of_ability_show_more_content_1= positive_current1_first_level_save, current_habits_of_ability_show_more_content_2= positive_current2_first_level_save, habitats_outside_of_me_show_more_content_1= positive_habitats1_first_level_save, habitats_outside_of_me_show_more_content_2= positive_habitats2_first_level_save)
                            if want_check:
                                want_save = Want.objects.filter(name=worksheet.cell_value(2,6), category=category_save, subcategory=sub_category_save, positive_i_want_show_more_content_1= positive_positive1_first_level_save,  positive_i_want_show_more_content_2= positive_positive2_first_level_save, steps_to_turn_positive_show_more_content_1= positive_steps1_first_level_save, steps_to_turn_positive_show_more_content_2=  positive_steps2_first_level_save, power_and_grace_show_more_content_1= positive_power1_first_level_save , power_and_grace_show_more_content_2= positive_power2_first_level_save, high_performance_ability_show_more_content_1= positive_high1_first_level_save, high_performance_ability_show_more_content_2= positive_high2_first_level_save, current_habits_of_ability_show_more_content_1= positive_current1_first_level_save, current_habits_of_ability_show_more_content_2= positive_current2_first_level_save, habitats_outside_of_me_show_more_content_1= positive_habitats1_first_level_save, habitats_outside_of_me_show_more_content_2= positive_habitats2_first_level_save)[0]
                                positive_check=True
                                warning.append(worksheet.cell_value(2,6)+ " want already exists")
                            if not want_check:
                                if worksheet.cell_value(2,8)!= "":
                                    positive_check=False
                                    want_save = Want.objects.create(name=worksheet.cell_value(2,6), order=worksheet.cell_value(2,8), category=category_save, subcategory=sub_category_save, positive_i_want_show_more_content_1= positive_positive1_first_level_save,  positive_i_want_show_more_content_2= positive_positive2_first_level_save, steps_to_turn_positive_show_more_content_1= positive_steps1_first_level_save, steps_to_turn_positive_show_more_content_2=  positive_steps2_first_level_save, power_and_grace_show_more_content_1= positive_power1_first_level_save , power_and_grace_show_more_content_2= positive_power2_first_level_save, high_performance_ability_show_more_content_1= positive_high1_first_level_save, high_performance_ability_show_more_content_2= positive_high2_first_level_save, current_habits_of_ability_show_more_content_1= positive_current1_first_level_save, current_habits_of_ability_show_more_content_2= positive_current2_first_level_save, habitats_outside_of_me_show_more_content_1= positive_habitats1_first_level_save, habitats_outside_of_me_show_more_content_2= positive_habitats2_first_level_save)
                                if worksheet.cell_value(2,8)== "":
                                    Errors.append("Please provide want order to insert")
                        except:
                            Errors.append("Error in want "+worksheet.cell_value(2,6)+" code")
                        if positive_check==False:
                            Success.append(want_save.name+ " want added successfully")
                        



                        try:
                            negative1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(8,1), first_field_content=worksheet.cell_value(9,1), second_field_content=worksheet.cell_value(14,1), third_field_content=worksheet.cell_value(19,1))
                            if negative1_first_level_check:
                                negative1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(8,1), first_field_content=worksheet.cell_value(9,1), second_field_content=worksheet.cell_value(14,1), third_field_content=worksheet.cell_value(19,1))[0]
                            if not negative1_first_level_check:
                                negative1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(8,1), first_field_content=worksheet.cell_value(9,1), second_field_content=worksheet.cell_value(14,1), third_field_content=worksheet.cell_value(19,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Negative First Level values")
                        
                        try:
                            negative2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(24,1), first_field_content=worksheet.cell_value(25,1), second_field_content=worksheet.cell_value(30,1), third_field_content=worksheet.cell_value(35,1))
                            if negative2_first_level_check:
                                negative2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(24,1), first_field_content=worksheet.cell_value(25,1), second_field_content=worksheet.cell_value(30,1), third_field_content=worksheet.cell_value(35,1))[0]
                            if not negative2_first_level_check:
                                negative2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(24,1), first_field_content=worksheet.cell_value(25,1), second_field_content=worksheet.cell_value(30,1), third_field_content=worksheet.cell_value(35,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Negative First Level values")
                        
                        try:
                            steps1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(42,1), first_field_content=worksheet.cell_value(43,1), second_field_content=worksheet.cell_value(48,1), third_field_content=worksheet.cell_value(53,1))
                            if steps1_first_level_check:
                                steps1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(42,1), first_field_content=worksheet.cell_value(43,1), second_field_content=worksheet.cell_value(48,1), third_field_content=worksheet.cell_value(53,1))[0]
                            if not steps1_first_level_check:
                                steps1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(42,1), first_field_content=worksheet.cell_value(43,1), second_field_content=worksheet.cell_value(48,1), third_field_content=worksheet.cell_value(53,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Steps First Level values")
                        
                        
                        try:
                            steps2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(58,1), first_field_content=worksheet.cell_value(59,1), second_field_content=worksheet.cell_value(64,1), third_field_content=worksheet.cell_value(69,1))
                            if steps2_first_level_check:
                                steps2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(58,1), first_field_content=worksheet.cell_value(59,1), second_field_content=worksheet.cell_value(64,1), third_field_content=worksheet.cell_value(69,1))[0]
                            if not steps2_first_level_check:
                                steps2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(58,1), first_field_content=worksheet.cell_value(59,1), second_field_content=worksheet.cell_value(64,1), third_field_content=worksheet.cell_value(69,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Steps First Level values")
                        
                        try:
                            weak1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(76,1), first_field_content=worksheet.cell_value(77,1), second_field_content=worksheet.cell_value(82,1), third_field_content=worksheet.cell_value(87,1))
                            if weak1_first_level_check:
                                weak1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(76,1), first_field_content=worksheet.cell_value(77,1), second_field_content=worksheet.cell_value(82,1), third_field_content=worksheet.cell_value(87,1))[0]
                            if not weak1_first_level_check:
                                weak1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(76,1), first_field_content=worksheet.cell_value(77,1), second_field_content=worksheet.cell_value(82,1), third_field_content=worksheet.cell_value(87,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Weak First Level values")
                        
                        try:
                            weak2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(92,1), first_field_content=worksheet.cell_value(93,1), second_field_content=worksheet.cell_value(98,1), third_field_content=worksheet.cell_value(103,1))
                            if weak2_first_level_check:
                                weak2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(92,1), first_field_content=worksheet.cell_value(93,1), second_field_content=worksheet.cell_value(98,1), third_field_content=worksheet.cell_value(103,1))[0]
                            if not weak2_first_level_check:
                                weak2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(92,1), first_field_content=worksheet.cell_value(93,1), second_field_content=worksheet.cell_value(98,1), third_field_content=worksheet.cell_value(103,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Weak First Level values")
                        
                        try:
                            low1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(110,1), first_field_content=worksheet.cell_value(111,1), second_field_content=worksheet.cell_value(116,1), third_field_content=worksheet.cell_value(121,1))
                            if low1_first_level_check:
                                low1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(110,1), first_field_content=worksheet.cell_value(111,1), second_field_content=worksheet.cell_value(116,1), third_field_content=worksheet.cell_value(121,1))[0]
                            if not low1_first_level_check:
                                low1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(110,1), first_field_content=worksheet.cell_value(111,1), second_field_content=worksheet.cell_value(116,1), third_field_content=worksheet.cell_value(121,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Low First Level values")
                        
                        try:
                            low2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(126,1), first_field_content=worksheet.cell_value(127,1), second_field_content=worksheet.cell_value(132,1), third_field_content=worksheet.cell_value(137,1))
                            if low2_first_level_check:
                                low2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(126,1), first_field_content=worksheet.cell_value(127,1), second_field_content=worksheet.cell_value(132,1), third_field_content=worksheet.cell_value(137,1))[0]
                            if not low2_first_level_check:
                                low2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(126,1), first_field_content=worksheet.cell_value(127,1), second_field_content=worksheet.cell_value(132,1), third_field_content=worksheet.cell_value(137,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Low First Level values")
                        
                        try:
                            current1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(144,1), first_field_content=worksheet.cell_value(145,1), second_field_content=worksheet.cell_value(150,1), third_field_content=worksheet.cell_value(155,1))
                            if current1_first_level_check:
                                current1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(144,1), first_field_content=worksheet.cell_value(145,1), second_field_content=worksheet.cell_value(150,1), third_field_content=worksheet.cell_value(155,1))[0]
                            if not current1_first_level_check:
                                current1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(144,1), first_field_content=worksheet.cell_value(145,1), second_field_content=worksheet.cell_value(150,1), third_field_content=worksheet.cell_value(155,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Current First Level values")
                        
                        try:
                            current2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(160,1), first_field_content=worksheet.cell_value(161,1), second_field_content=worksheet.cell_value(166,1), third_field_content=worksheet.cell_value(171,1))
                            if current2_first_level_check:
                                current2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(160,1), first_field_content=worksheet.cell_value(161,1), second_field_content=worksheet.cell_value(166,1), third_field_content=worksheet.cell_value(171,1))[0]
                            if not current2_first_level_check:
                                current2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(160,1), first_field_content=worksheet.cell_value(161,1), second_field_content=worksheet.cell_value(166,1), third_field_content=worksheet.cell_value(171,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Current First Level values")
                        
                        try:
                            habitats1_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(178,1), first_field_content=worksheet.cell_value(179,1), second_field_content=worksheet.cell_value(184,1), third_field_content=worksheet.cell_value(189,1))
                            if habitats1_first_level_check:
                                habitats1_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(178,1), first_field_content=worksheet.cell_value(179,1), second_field_content=worksheet.cell_value(184,1), third_field_content=worksheet.cell_value(189,1))[0]
                            if not habitats1_first_level_check:
                                habitats1_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(178,1), first_field_content=worksheet.cell_value(179,1), second_field_content=worksheet.cell_value(184,1), third_field_content=worksheet.cell_value(189,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Habitats First Level values")
                        
                        try:
                            habitats2_first_level_check = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(194,1), first_field_content=worksheet.cell_value(195,1), second_field_content=worksheet.cell_value(200,1), third_field_content=worksheet.cell_value(205,1))
                            if habitats2_first_level_check:
                                habitats2_first_level_save = FirstLevelContent.objects.filter(show_less_content=worksheet.cell_value(194,1), first_field_content=worksheet.cell_value(195,1), second_field_content=worksheet.cell_value(200,1), third_field_content=worksheet.cell_value(205,1))[0]
                            if not habitats2_first_level_check:
                                habitats2_first_level_save = FirstLevelContent.objects.create(show_less_content=worksheet.cell_value(194,1), first_field_content=worksheet.cell_value(195,1), second_field_content=worksheet.cell_value(200,1), third_field_content=worksheet.cell_value(205,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Habitats First Level values")
                        
                        try:
                            negative1_second_level_check = SecondLevelContent.objects.filter(first_level=negative1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,1), second_f1_show_more_text=worksheet.cell_value(11,1), third_f1_show_more_text=worksheet.cell_value(12,1), first_f2_show_more_text=worksheet.cell_value(15,1), second_f2_show_more_text=worksheet.cell_value(16,1), third_f2_show_more_text=worksheet.cell_value(17,1), first_f3_show_more_text=worksheet.cell_value(20,1), second_f3_show_more_text=worksheet.cell_value(21,1), third_f3_show_more_text=worksheet.cell_value(22,1))
                            if negative1_second_level_check:
                                negative1_second_level_save = SecondLevelContent.objects.filter(first_level=negative1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,1), second_f1_show_more_text=worksheet.cell_value(11,1), third_f1_show_more_text=worksheet.cell_value(12,1), first_f2_show_more_text=worksheet.cell_value(15,1), second_f2_show_more_text=worksheet.cell_value(16,1), third_f2_show_more_text=worksheet.cell_value(17,1), first_f3_show_more_text=worksheet.cell_value(20,1), second_f3_show_more_text=worksheet.cell_value(21,1), third_f3_show_more_text=worksheet.cell_value(22,1))[0]
                            if not negative1_second_level_check:
                                negative1_second_level_save = SecondLevelContent.objects.create(first_level=negative1_first_level_save, first_f1_show_more_text=worksheet.cell_value(10,1), second_f1_show_more_text=worksheet.cell_value(11,1), third_f1_show_more_text=worksheet.cell_value(12,1), first_f2_show_more_text=worksheet.cell_value(15,1), second_f2_show_more_text=worksheet.cell_value(16,1), third_f2_show_more_text=worksheet.cell_value(17,1), first_f3_show_more_text=worksheet.cell_value(20,1), second_f3_show_more_text=worksheet.cell_value(21,1), third_f3_show_more_text=worksheet.cell_value(22,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Negative Second Level values")
                        
                        try:
                            negative2_second_level_check = SecondLevelContent.objects.filter(first_level=negative2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,1), second_f1_show_more_text=worksheet.cell_value(27,1), third_f1_show_more_text=worksheet.cell_value(28,1), first_f2_show_more_text=worksheet.cell_value(31,1), second_f2_show_more_text=worksheet.cell_value(32,1), third_f2_show_more_text=worksheet.cell_value(33,1), first_f3_show_more_text=worksheet.cell_value(36,1), second_f3_show_more_text=worksheet.cell_value(37,1), third_f3_show_more_text=worksheet.cell_value(38,1))
                            if negative2_second_level_check:
                                negative2_second_level_save = SecondLevelContent.objects.filter(first_level=negative2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,1), second_f1_show_more_text=worksheet.cell_value(27,1), third_f1_show_more_text=worksheet.cell_value(28,1), first_f2_show_more_text=worksheet.cell_value(31,1), second_f2_show_more_text=worksheet.cell_value(32,1), third_f2_show_more_text=worksheet.cell_value(33,1), first_f3_show_more_text=worksheet.cell_value(36,1), second_f3_show_more_text=worksheet.cell_value(37,1), third_f3_show_more_text=worksheet.cell_value(38,1))[0]
                            if not negative2_second_level_check:
                                negative2_second_level_save = SecondLevelContent.objects.create(first_level=negative2_first_level_save, first_f1_show_more_text=worksheet.cell_value(26,1), second_f1_show_more_text=worksheet.cell_value(27,1), third_f1_show_more_text=worksheet.cell_value(28,1), first_f2_show_more_text=worksheet.cell_value(31,1), second_f2_show_more_text=worksheet.cell_value(32,1), third_f2_show_more_text=worksheet.cell_value(33,1), first_f3_show_more_text=worksheet.cell_value(36,1), second_f3_show_more_text=worksheet.cell_value(37,1), third_f3_show_more_text=worksheet.cell_value(38,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Negative Second Level values")
                        
                        try:
                            steps1_second_level_check = SecondLevelContent.objects.filter(first_level=steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,1), second_f1_show_more_text=worksheet.cell_value(45,1), third_f1_show_more_text=worksheet.cell_value(46,1), first_f2_show_more_text=worksheet.cell_value(49,1), second_f2_show_more_text=worksheet.cell_value(50,1), third_f2_show_more_text=worksheet.cell_value(51,1), first_f3_show_more_text=worksheet.cell_value(54,1), second_f3_show_more_text=worksheet.cell_value(55,1), third_f3_show_more_text=worksheet.cell_value(56,1))
                            if steps1_second_level_check:
                                steps1_second_level_save = SecondLevelContent.objects.filter(first_level=steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,1), second_f1_show_more_text=worksheet.cell_value(45,1), third_f1_show_more_text=worksheet.cell_value(46,1), first_f2_show_more_text=worksheet.cell_value(49,1), second_f2_show_more_text=worksheet.cell_value(50,1), third_f2_show_more_text=worksheet.cell_value(51,1), first_f3_show_more_text=worksheet.cell_value(54,1), second_f3_show_more_text=worksheet.cell_value(55,1), third_f3_show_more_text=worksheet.cell_value(56,1))[0]
                            if not steps1_second_level_check:
                                steps1_second_level_save = SecondLevelContent.objects.create(first_level=steps1_first_level_save, first_f1_show_more_text=worksheet.cell_value(44,1), second_f1_show_more_text=worksheet.cell_value(45,1), third_f1_show_more_text=worksheet.cell_value(46,1), first_f2_show_more_text=worksheet.cell_value(49,1), second_f2_show_more_text=worksheet.cell_value(50,1), third_f2_show_more_text=worksheet.cell_value(51,1), first_f3_show_more_text=worksheet.cell_value(54,1), second_f3_show_more_text=worksheet.cell_value(55,1), third_f3_show_more_text=worksheet.cell_value(56,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Steps Second Level values")
                        
                        try:
                            steps2_second_level_check = SecondLevelContent.objects.filter(first_level=steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,1), second_f1_show_more_text=worksheet.cell_value(61,1), third_f1_show_more_text=worksheet.cell_value(62,1), first_f2_show_more_text=worksheet.cell_value(65,1), second_f2_show_more_text=worksheet.cell_value(66,1), third_f2_show_more_text=worksheet.cell_value(67,1), first_f3_show_more_text=worksheet.cell_value(70,1), second_f3_show_more_text=worksheet.cell_value(71,1), third_f3_show_more_text=worksheet.cell_value(72,1))
                            if steps2_second_level_check:
                                steps2_second_level_save = SecondLevelContent.objects.filter(first_level=steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,1), second_f1_show_more_text=worksheet.cell_value(61,1), third_f1_show_more_text=worksheet.cell_value(62,1), first_f2_show_more_text=worksheet.cell_value(65,1), second_f2_show_more_text=worksheet.cell_value(66,1), third_f2_show_more_text=worksheet.cell_value(67,1), first_f3_show_more_text=worksheet.cell_value(70,1), second_f3_show_more_text=worksheet.cell_value(71,1), third_f3_show_more_text=worksheet.cell_value(72,1))[0]
                            if not steps2_second_level_check:
                                steps2_second_level_save = SecondLevelContent.objects.create(first_level=steps2_first_level_save, first_f1_show_more_text=worksheet.cell_value(60,1), second_f1_show_more_text=worksheet.cell_value(61,1), third_f1_show_more_text=worksheet.cell_value(62,1), first_f2_show_more_text=worksheet.cell_value(65,1), second_f2_show_more_text=worksheet.cell_value(66,1), third_f2_show_more_text=worksheet.cell_value(67,1), first_f3_show_more_text=worksheet.cell_value(70,1), second_f3_show_more_text=worksheet.cell_value(71,1), third_f3_show_more_text=worksheet.cell_value(72,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Steps Second Level values")
                        
                        try:
                            weak1_second_level_check = SecondLevelContent.objects.filter(first_level=weak1_first_level_save, first_f1_show_more_text=worksheet.cell_value(78,1), second_f1_show_more_text=worksheet.cell_value(79,1), third_f1_show_more_text=worksheet.cell_value(80,1), first_f2_show_more_text=worksheet.cell_value(83,1), second_f2_show_more_text=worksheet.cell_value(84,1), third_f2_show_more_text=worksheet.cell_value(85,1), first_f3_show_more_text=worksheet.cell_value(88,1), second_f3_show_more_text=worksheet.cell_value(89,1), third_f3_show_more_text=worksheet.cell_value(90,1))
                            if weak1_second_level_check:
                                weak1_second_level_save = SecondLevelContent.objects.filter(first_level=weak1_first_level_save, first_f1_show_more_text=worksheet.cell_value(78,1), second_f1_show_more_text=worksheet.cell_value(79,1), third_f1_show_more_text=worksheet.cell_value(80,1), first_f2_show_more_text=worksheet.cell_value(83,1), second_f2_show_more_text=worksheet.cell_value(84,1), third_f2_show_more_text=worksheet.cell_value(85,1), first_f3_show_more_text=worksheet.cell_value(88,1), second_f3_show_more_text=worksheet.cell_value(89,1), third_f3_show_more_text=worksheet.cell_value(90,1))[0]
                            if not weak1_second_level_check:
                                weak1_second_level_save = SecondLevelContent.objects.create(first_level=weak1_first_level_save, first_f1_show_more_text=worksheet.cell_value(78,1), second_f1_show_more_text=worksheet.cell_value(79,1), third_f1_show_more_text=worksheet.cell_value(80,1), first_f2_show_more_text=worksheet.cell_value(83,1), second_f2_show_more_text=worksheet.cell_value(84,1), third_f2_show_more_text=worksheet.cell_value(85,1), first_f3_show_more_text=worksheet.cell_value(88,1), second_f3_show_more_text=worksheet.cell_value(89,1), third_f3_show_more_text=worksheet.cell_value(90,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Weak Second Level values")
                        
                        try:
                            weak2_second_level_check = SecondLevelContent.objects.filter(first_level=weak2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,1), second_f1_show_more_text=worksheet.cell_value(95,1), third_f1_show_more_text=worksheet.cell_value(96,1), first_f2_show_more_text=worksheet.cell_value(99,1), second_f2_show_more_text=worksheet.cell_value(100,1), third_f2_show_more_text=worksheet.cell_value(101,1), first_f3_show_more_text=worksheet.cell_value(104,1), second_f3_show_more_text=worksheet.cell_value(105,1), third_f3_show_more_text=worksheet.cell_value(106,1))
                            if weak2_second_level_check:
                                weak2_second_level_save = SecondLevelContent.objects.filter(first_level=weak2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,1), second_f1_show_more_text=worksheet.cell_value(95,1), third_f1_show_more_text=worksheet.cell_value(96,1), first_f2_show_more_text=worksheet.cell_value(99,1), second_f2_show_more_text=worksheet.cell_value(100,1), third_f2_show_more_text=worksheet.cell_value(101,1), first_f3_show_more_text=worksheet.cell_value(104,1), second_f3_show_more_text=worksheet.cell_value(105,1), third_f3_show_more_text=worksheet.cell_value(106,1))[0]
                            if not weak2_second_level_check:
                                weak2_second_level_save = SecondLevelContent.objects.create(first_level=weak2_first_level_save, first_f1_show_more_text=worksheet.cell_value(94,1), second_f1_show_more_text=worksheet.cell_value(95,1), third_f1_show_more_text=worksheet.cell_value(96,1), first_f2_show_more_text=worksheet.cell_value(99,1), second_f2_show_more_text=worksheet.cell_value(100,1), third_f2_show_more_text=worksheet.cell_value(101,1), first_f3_show_more_text=worksheet.cell_value(104,1), second_f3_show_more_text=worksheet.cell_value(105,1), third_f3_show_more_text=worksheet.cell_value(106,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Weak Second Level values")
                        
                        try:
                            low1_second_level_check = SecondLevelContent.objects.filter(first_level=low1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,1), second_f1_show_more_text=worksheet.cell_value(113,1), third_f1_show_more_text=worksheet.cell_value(114,1), first_f2_show_more_text=worksheet.cell_value(117,1), second_f2_show_more_text=worksheet.cell_value(118,1), third_f2_show_more_text=worksheet.cell_value(119,1), first_f3_show_more_text=worksheet.cell_value(122,1), second_f3_show_more_text=worksheet.cell_value(123,1), third_f3_show_more_text=worksheet.cell_value(124,1))
                            if low1_second_level_check:
                                low1_second_level_save = SecondLevelContent.objects.filter(first_level=low1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,1), second_f1_show_more_text=worksheet.cell_value(113,1), third_f1_show_more_text=worksheet.cell_value(114,1), first_f2_show_more_text=worksheet.cell_value(117,1), second_f2_show_more_text=worksheet.cell_value(118,1), third_f2_show_more_text=worksheet.cell_value(119,1), first_f3_show_more_text=worksheet.cell_value(122,1), second_f3_show_more_text=worksheet.cell_value(123,1), third_f3_show_more_text=worksheet.cell_value(124,1))[0]
                            else:
                                low1_second_level_save = SecondLevelContent.objects.create(first_level=low1_first_level_save, first_f1_show_more_text=worksheet.cell_value(112,1), second_f1_show_more_text=worksheet.cell_value(113,1), third_f1_show_more_text=worksheet.cell_value(114,1), first_f2_show_more_text=worksheet.cell_value(117,1), second_f2_show_more_text=worksheet.cell_value(118,1), third_f2_show_more_text=worksheet.cell_value(119,1), first_f3_show_more_text=worksheet.cell_value(122,1), second_f3_show_more_text=worksheet.cell_value(123,1), third_f3_show_more_text=worksheet.cell_value(124,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Low Second Level values")
                        
                        try:
                            low2_second_level_check = SecondLevelContent.objects.filter(first_level=low2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,1), second_f1_show_more_text=worksheet.cell_value(129,1), third_f1_show_more_text=worksheet.cell_value(130,1), first_f2_show_more_text=worksheet.cell_value(133,1), second_f2_show_more_text=worksheet.cell_value(134,1), third_f2_show_more_text=worksheet.cell_value(135,1), first_f3_show_more_text=worksheet.cell_value(138,1), second_f3_show_more_text=worksheet.cell_value(139,1), third_f3_show_more_text=worksheet.cell_value(140,1))
                            if low2_second_level_check:
                                low2_second_level_save = SecondLevelContent.objects.filter(first_level=low2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,1), second_f1_show_more_text=worksheet.cell_value(129,1), third_f1_show_more_text=worksheet.cell_value(130,1), first_f2_show_more_text=worksheet.cell_value(133,1), second_f2_show_more_text=worksheet.cell_value(134,1), third_f2_show_more_text=worksheet.cell_value(135,1), first_f3_show_more_text=worksheet.cell_value(138,1), second_f3_show_more_text=worksheet.cell_value(139,1), third_f3_show_more_text=worksheet.cell_value(140,1))[0]
                            else:
                                low2_second_level_save = SecondLevelContent.objects.create(first_level=low2_first_level_save, first_f1_show_more_text=worksheet.cell_value(128,1), second_f1_show_more_text=worksheet.cell_value(129,1), third_f1_show_more_text=worksheet.cell_value(130,1), first_f2_show_more_text=worksheet.cell_value(133,1), second_f2_show_more_text=worksheet.cell_value(134,1), third_f2_show_more_text=worksheet.cell_value(135,1), first_f3_show_more_text=worksheet.cell_value(138,1), second_f3_show_more_text=worksheet.cell_value(139,1), third_f3_show_more_text=worksheet.cell_value(140,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Low Second Level values")
                        
                        try:
                            current1_second_level_check = SecondLevelContent.objects.filter(first_level=current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,1), second_f1_show_more_text=worksheet.cell_value(147,1), third_f1_show_more_text=worksheet.cell_value(148,1), first_f2_show_more_text=worksheet.cell_value(151,1), second_f2_show_more_text=worksheet.cell_value(152,1), third_f2_show_more_text=worksheet.cell_value(153,1), first_f3_show_more_text=worksheet.cell_value(156,1), second_f3_show_more_text=worksheet.cell_value(157,1), third_f3_show_more_text=worksheet.cell_value(158,1))
                            if current1_second_level_check:
                                current1_second_level_save = SecondLevelContent.objects.filter(first_level=current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,1), second_f1_show_more_text=worksheet.cell_value(147,1), third_f1_show_more_text=worksheet.cell_value(148,1), first_f2_show_more_text=worksheet.cell_value(151,1), second_f2_show_more_text=worksheet.cell_value(152,1), third_f2_show_more_text=worksheet.cell_value(153,1), first_f3_show_more_text=worksheet.cell_value(156,1), second_f3_show_more_text=worksheet.cell_value(157,1), third_f3_show_more_text=worksheet.cell_value(158,1))[0]
                            else:
                                current1_second_level_save = SecondLevelContent.objects.create(first_level=current1_first_level_save, first_f1_show_more_text=worksheet.cell_value(146,1), second_f1_show_more_text=worksheet.cell_value(147,1), third_f1_show_more_text=worksheet.cell_value(148,1), first_f2_show_more_text=worksheet.cell_value(151,1), second_f2_show_more_text=worksheet.cell_value(152,1), third_f2_show_more_text=worksheet.cell_value(153,1), first_f3_show_more_text=worksheet.cell_value(156,1), second_f3_show_more_text=worksheet.cell_value(157,1), third_f3_show_more_text=worksheet.cell_value(158,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Current Second Level values")
                        
                        try:
                            current2_second_level_check = SecondLevelContent.objects.filter(first_level=current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,1), second_f1_show_more_text=worksheet.cell_value(163,1), third_f1_show_more_text=worksheet.cell_value(164,1), first_f2_show_more_text=worksheet.cell_value(167,1), second_f2_show_more_text=worksheet.cell_value(168,1), third_f2_show_more_text=worksheet.cell_value(169,1), first_f3_show_more_text=worksheet.cell_value(172,1), second_f3_show_more_text=worksheet.cell_value(173,1), third_f3_show_more_text=worksheet.cell_value(174,1))
                            if current2_second_level_check:
                                current2_second_level_save = SecondLevelContent.objects.filter(first_level=current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,1), second_f1_show_more_text=worksheet.cell_value(163,1), third_f1_show_more_text=worksheet.cell_value(164,1), first_f2_show_more_text=worksheet.cell_value(167,1), second_f2_show_more_text=worksheet.cell_value(168,1), third_f2_show_more_text=worksheet.cell_value(169,1), first_f3_show_more_text=worksheet.cell_value(172,1), second_f3_show_more_text=worksheet.cell_value(173,1), third_f3_show_more_text=worksheet.cell_value(174,1))[0]
                            else:
                                current2_second_level_save = SecondLevelContent.objects.create(first_level=current2_first_level_save, first_f1_show_more_text=worksheet.cell_value(162,1), second_f1_show_more_text=worksheet.cell_value(163,1), third_f1_show_more_text=worksheet.cell_value(164,1), first_f2_show_more_text=worksheet.cell_value(167,1), second_f2_show_more_text=worksheet.cell_value(168,1), third_f2_show_more_text=worksheet.cell_value(169,1), first_f3_show_more_text=worksheet.cell_value(172,1), second_f3_show_more_text=worksheet.cell_value(173,1), third_f3_show_more_text=worksheet.cell_value(174,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Current Second Level values")
                        
                        try:
                            habitats1_second_level_check = SecondLevelContent.objects.filter(first_level=habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,1), second_f1_show_more_text=worksheet.cell_value(181,1), third_f1_show_more_text=worksheet.cell_value(182,1), first_f2_show_more_text=worksheet.cell_value(185,1), second_f2_show_more_text=worksheet.cell_value(186,1), third_f2_show_more_text=worksheet.cell_value(187,1), first_f3_show_more_text=worksheet.cell_value(190,1), second_f3_show_more_text=worksheet.cell_value(191,1), third_f3_show_more_text=worksheet.cell_value(192,1))
                            if habitats1_second_level_check:
                                habitats1_second_level_save = SecondLevelContent.objects.filter(first_level=habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,1), second_f1_show_more_text=worksheet.cell_value(181,1), third_f1_show_more_text=worksheet.cell_value(182,1), first_f2_show_more_text=worksheet.cell_value(185,1), second_f2_show_more_text=worksheet.cell_value(186,1), third_f2_show_more_text=worksheet.cell_value(187,1), first_f3_show_more_text=worksheet.cell_value(190,1), second_f3_show_more_text=worksheet.cell_value(191,1), third_f3_show_more_text=worksheet.cell_value(192,1))[0]
                            else:
                                habitats1_second_level_save = SecondLevelContent.objects.create(first_level=habitats1_first_level_save, first_f1_show_more_text=worksheet.cell_value(180,1), second_f1_show_more_text=worksheet.cell_value(181,1), third_f1_show_more_text=worksheet.cell_value(182,1), first_f2_show_more_text=worksheet.cell_value(185,1), second_f2_show_more_text=worksheet.cell_value(186,1), third_f2_show_more_text=worksheet.cell_value(187,1), first_f3_show_more_text=worksheet.cell_value(190,1), second_f3_show_more_text=worksheet.cell_value(191,1), third_f3_show_more_text=worksheet.cell_value(192,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Habitats Second Level values")
                        
                        try:
                            habitats2_second_level_check = SecondLevelContent.objects.filter(first_level=habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,1), second_f1_show_more_text=worksheet.cell_value(197,1), third_f1_show_more_text=worksheet.cell_value(198,1), first_f2_show_more_text=worksheet.cell_value(201,1), second_f2_show_more_text=worksheet.cell_value(202,1), third_f2_show_more_text=worksheet.cell_value(203,1), first_f3_show_more_text=worksheet.cell_value(206,1), second_f3_show_more_text=worksheet.cell_value(207,1), third_f3_show_more_text=worksheet.cell_value(208,1))
                            if habitats2_second_level_check:
                                habitats2_second_level_save = SecondLevelContent.objects.filter(first_level=habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,1), second_f1_show_more_text=worksheet.cell_value(197,1), third_f1_show_more_text=worksheet.cell_value(198,1), first_f2_show_more_text=worksheet.cell_value(201,1), second_f2_show_more_text=worksheet.cell_value(202,1), third_f2_show_more_text=worksheet.cell_value(203,1), first_f3_show_more_text=worksheet.cell_value(206,1), second_f3_show_more_text=worksheet.cell_value(207,1), third_f3_show_more_text=worksheet.cell_value(208,1))[0]
                            else:
                                habitats2_second_level_save = SecondLevelContent.objects.create(first_level=habitats2_first_level_save, first_f1_show_more_text=worksheet.cell_value(196,1), second_f1_show_more_text=worksheet.cell_value(197,1), third_f1_show_more_text=worksheet.cell_value(198,1), first_f2_show_more_text=worksheet.cell_value(201,1), second_f2_show_more_text=worksheet.cell_value(202,1), third_f2_show_more_text=worksheet.cell_value(203,1), first_f3_show_more_text=worksheet.cell_value(206,1), second_f3_show_more_text=worksheet.cell_value(207,1), third_f3_show_more_text=worksheet.cell_value(208,1))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Habitats Second Level values")
                        
                        try:
                            negative1_third_level_check = ThirdLevelContent.objects.filter(second_level=negative1_second_level_save, f1_1st_f1_text=worksheet.cell_value(10,2), f1_1st_f2_text=worksheet.cell_value(10,3), f1_1st_f3_text=worksheet.cell_value(10,4), f1_2nd_f1_text=worksheet.cell_value(11,2), f1_2nd_f2_text=worksheet.cell_value(11,3), f1_2nd_f3_text=worksheet.cell_value(11,4), f1_3rd_f1_text=worksheet.cell_value(12,2), f1_3rd_f2_text=worksheet.cell_value(12,3), f1_3rd_f3_text=worksheet.cell_value(12,4), f2_1st_f1_text=worksheet.cell_value(15,2), f2_1st_f2_text=worksheet.cell_value(15,3), f2_1st_f3_text=worksheet.cell_value(15,4), f2_2nd_f1_text=worksheet.cell_value(16,2), f2_2nd_f2_text=worksheet.cell_value(16,3), f2_2nd_f3_text=worksheet.cell_value(16,4), f2_3rd_f1_text=worksheet.cell_value(17,2), f2_3rd_f2_text=worksheet.cell_value(17,3), f2_3rd_f3_text=worksheet.cell_value(17,4), f3_1st_f1_text=worksheet.cell_value(20,2), f3_1st_f2_text=worksheet.cell_value(20,3), f3_1st_f3_text=worksheet.cell_value(20,4), f3_2nd_f1_text=worksheet.cell_value(21,2), f3_2nd_f2_text=worksheet.cell_value(21,3), f3_2nd_f3_text=worksheet.cell_value(21,4), f3_3rd_f1_text=worksheet.cell_value(22,2), f3_3rd_f2_text=worksheet.cell_value(22,3), f3_3rd_f3_text=worksheet.cell_value(22,4))
                            if negative1_third_level_check:
                                negative1_third_level_save = ThirdLevelContent.objects.filter(second_level=negative1_second_level_save, f1_1st_f1_text=worksheet.cell_value(10,2), f1_1st_f2_text=worksheet.cell_value(10,3), f1_1st_f3_text=worksheet.cell_value(10,4), f1_2nd_f1_text=worksheet.cell_value(11,2), f1_2nd_f2_text=worksheet.cell_value(11,3), f1_2nd_f3_text=worksheet.cell_value(11,4), f1_3rd_f1_text=worksheet.cell_value(12,2), f1_3rd_f2_text=worksheet.cell_value(12,3), f1_3rd_f3_text=worksheet.cell_value(12,4), f2_1st_f1_text=worksheet.cell_value(15,2), f2_1st_f2_text=worksheet.cell_value(15,3), f2_1st_f3_text=worksheet.cell_value(15,4), f2_2nd_f1_text=worksheet.cell_value(16,2), f2_2nd_f2_text=worksheet.cell_value(16,3), f2_2nd_f3_text=worksheet.cell_value(16,4), f2_3rd_f1_text=worksheet.cell_value(17,2), f2_3rd_f2_text=worksheet.cell_value(17,3), f2_3rd_f3_text=worksheet.cell_value(17,4), f3_1st_f1_text=worksheet.cell_value(20,2), f3_1st_f2_text=worksheet.cell_value(20,3), f3_1st_f3_text=worksheet.cell_value(20,4), f3_2nd_f1_text=worksheet.cell_value(21,2), f3_2nd_f2_text=worksheet.cell_value(21,3), f3_2nd_f3_text=worksheet.cell_value(21,4), f3_3rd_f1_text=worksheet.cell_value(22,2), f3_3rd_f2_text=worksheet.cell_value(22,3), f3_3rd_f3_text=worksheet.cell_value(22,4))[0]
                            else:
                                negative1_third_level_save = ThirdLevelContent.objects.create(second_level=negative1_second_level_save, f1_1st_f1_text=worksheet.cell_value(10,2), f1_1st_f2_text=worksheet.cell_value(10,3), f1_1st_f3_text=worksheet.cell_value(10,4), f1_2nd_f1_text=worksheet.cell_value(11,2), f1_2nd_f2_text=worksheet.cell_value(11,3), f1_2nd_f3_text=worksheet.cell_value(11,4), f1_3rd_f1_text=worksheet.cell_value(12,2), f1_3rd_f2_text=worksheet.cell_value(12,3), f1_3rd_f3_text=worksheet.cell_value(12,4), f2_1st_f1_text=worksheet.cell_value(15,2), f2_1st_f2_text=worksheet.cell_value(15,3), f2_1st_f3_text=worksheet.cell_value(15,4), f2_2nd_f1_text=worksheet.cell_value(16,2), f2_2nd_f2_text=worksheet.cell_value(16,3), f2_2nd_f3_text=worksheet.cell_value(16,4), f2_3rd_f1_text=worksheet.cell_value(17,2), f2_3rd_f2_text=worksheet.cell_value(17,3), f2_3rd_f3_text=worksheet.cell_value(17,4), f3_1st_f1_text=worksheet.cell_value(20,2), f3_1st_f2_text=worksheet.cell_value(20,3), f3_1st_f3_text=worksheet.cell_value(20,4), f3_2nd_f1_text=worksheet.cell_value(21,2), f3_2nd_f2_text=worksheet.cell_value(21,3), f3_2nd_f3_text=worksheet.cell_value(21,4), f3_3rd_f1_text=worksheet.cell_value(22,2), f3_3rd_f2_text=worksheet.cell_value(22,3), f3_3rd_f3_text=worksheet.cell_value(22,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Nagative Third Level values")
                        
                        try:
                            negative2_third_level_check = ThirdLevelContent.objects.filter(second_level=negative2_second_level_save, f1_1st_f1_text=worksheet.cell_value(26,2), f1_1st_f2_text=worksheet.cell_value(26,3), f1_1st_f3_text=worksheet.cell_value(26,4), f1_2nd_f1_text=worksheet.cell_value(27,2), f1_2nd_f2_text=worksheet.cell_value(27,3), f1_2nd_f3_text=worksheet.cell_value(27,4), f1_3rd_f1_text=worksheet.cell_value(28,2), f1_3rd_f2_text=worksheet.cell_value(28,3), f1_3rd_f3_text=worksheet.cell_value(28,4), f2_1st_f1_text=worksheet.cell_value(31,2), f2_1st_f2_text=worksheet.cell_value(31,3), f2_1st_f3_text=worksheet.cell_value(31,4), f2_2nd_f1_text=worksheet.cell_value(32,2), f2_2nd_f2_text=worksheet.cell_value(32,3), f2_2nd_f3_text=worksheet.cell_value(32,4), f2_3rd_f1_text=worksheet.cell_value(33,2), f2_3rd_f2_text=worksheet.cell_value(33,3), f2_3rd_f3_text=worksheet.cell_value(33,4), f3_1st_f1_text=worksheet.cell_value(36,2), f3_1st_f2_text=worksheet.cell_value(36,3), f3_1st_f3_text=worksheet.cell_value(36,4), f3_2nd_f1_text=worksheet.cell_value(37,2), f3_2nd_f2_text=worksheet.cell_value(37,3), f3_2nd_f3_text=worksheet.cell_value(37,4), f3_3rd_f1_text=worksheet.cell_value(38,2), f3_3rd_f2_text=worksheet.cell_value(38,3), f3_3rd_f3_text=worksheet.cell_value(38,4))
                            if negative2_third_level_check:
                                negative2_third_level_save = ThirdLevelContent.objects.filter(second_level=negative2_second_level_save, f1_1st_f1_text=worksheet.cell_value(26,2), f1_1st_f2_text=worksheet.cell_value(26,3), f1_1st_f3_text=worksheet.cell_value(26,4), f1_2nd_f1_text=worksheet.cell_value(27,2), f1_2nd_f2_text=worksheet.cell_value(27,3), f1_2nd_f3_text=worksheet.cell_value(27,4), f1_3rd_f1_text=worksheet.cell_value(28,2), f1_3rd_f2_text=worksheet.cell_value(28,3), f1_3rd_f3_text=worksheet.cell_value(28,4), f2_1st_f1_text=worksheet.cell_value(31,2), f2_1st_f2_text=worksheet.cell_value(31,3), f2_1st_f3_text=worksheet.cell_value(31,4), f2_2nd_f1_text=worksheet.cell_value(32,2), f2_2nd_f2_text=worksheet.cell_value(32,3), f2_2nd_f3_text=worksheet.cell_value(32,4), f2_3rd_f1_text=worksheet.cell_value(33,2), f2_3rd_f2_text=worksheet.cell_value(33,3), f2_3rd_f3_text=worksheet.cell_value(33,4), f3_1st_f1_text=worksheet.cell_value(36,2), f3_1st_f2_text=worksheet.cell_value(36,3), f3_1st_f3_text=worksheet.cell_value(36,4), f3_2nd_f1_text=worksheet.cell_value(37,2), f3_2nd_f2_text=worksheet.cell_value(37,3), f3_2nd_f3_text=worksheet.cell_value(37,4), f3_3rd_f1_text=worksheet.cell_value(38,2), f3_3rd_f2_text=worksheet.cell_value(38,3), f3_3rd_f3_text=worksheet.cell_value(38,4))[0]
                            else:
                                negative2_third_level_save = ThirdLevelContent.objects.create(second_level=negative2_second_level_save, f1_1st_f1_text=worksheet.cell_value(26,2), f1_1st_f2_text=worksheet.cell_value(26,3), f1_1st_f3_text=worksheet.cell_value(26,4), f1_2nd_f1_text=worksheet.cell_value(27,2), f1_2nd_f2_text=worksheet.cell_value(27,3), f1_2nd_f3_text=worksheet.cell_value(27,4), f1_3rd_f1_text=worksheet.cell_value(28,2), f1_3rd_f2_text=worksheet.cell_value(28,3), f1_3rd_f3_text=worksheet.cell_value(28,4), f2_1st_f1_text=worksheet.cell_value(31,2), f2_1st_f2_text=worksheet.cell_value(31,3), f2_1st_f3_text=worksheet.cell_value(31,4), f2_2nd_f1_text=worksheet.cell_value(32,2), f2_2nd_f2_text=worksheet.cell_value(32,3), f2_2nd_f3_text=worksheet.cell_value(32,4), f2_3rd_f1_text=worksheet.cell_value(33,2), f2_3rd_f2_text=worksheet.cell_value(33,3), f2_3rd_f3_text=worksheet.cell_value(33,4), f3_1st_f1_text=worksheet.cell_value(36,2), f3_1st_f2_text=worksheet.cell_value(36,3), f3_1st_f3_text=worksheet.cell_value(36,4), f3_2nd_f1_text=worksheet.cell_value(37,2), f3_2nd_f2_text=worksheet.cell_value(37,3), f3_2nd_f3_text=worksheet.cell_value(37,4), f3_3rd_f1_text=worksheet.cell_value(38,2), f3_3rd_f2_text=worksheet.cell_value(38,3), f3_3rd_f3_text=worksheet.cell_value(38,4))
                            
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Negative Third Level values")
                        
                        try:
                            steps1_third_level_check = ThirdLevelContent.objects.filter(second_level=steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,2), f1_1st_f2_text=worksheet.cell_value(44,3), f1_1st_f3_text=worksheet.cell_value(44,4), f1_2nd_f1_text=worksheet.cell_value(45,2), f1_2nd_f2_text=worksheet.cell_value(45,3), f1_2nd_f3_text=worksheet.cell_value(45,4), f1_3rd_f1_text=worksheet.cell_value(46,2), f1_3rd_f2_text=worksheet.cell_value(46,3), f1_3rd_f3_text=worksheet.cell_value(46,4), f2_1st_f1_text=worksheet.cell_value(49,2), f2_1st_f2_text=worksheet.cell_value(49,3), f2_1st_f3_text=worksheet.cell_value(49,4), f2_2nd_f1_text=worksheet.cell_value(50,2), f2_2nd_f2_text=worksheet.cell_value(50,3), f2_2nd_f3_text=worksheet.cell_value(50,4), f2_3rd_f1_text=worksheet.cell_value(51,2), f2_3rd_f2_text=worksheet.cell_value(51,3), f2_3rd_f3_text=worksheet.cell_value(51,4), f3_1st_f1_text=worksheet.cell_value(54,2), f3_1st_f2_text=worksheet.cell_value(54,3), f3_1st_f3_text=worksheet.cell_value(54,4), f3_2nd_f1_text=worksheet.cell_value(55,2), f3_2nd_f2_text=worksheet.cell_value(55,3), f3_2nd_f3_text=worksheet.cell_value(55,4), f3_3rd_f1_text=worksheet.cell_value(56,2), f3_3rd_f2_text=worksheet.cell_value(56,3), f3_3rd_f3_text=worksheet.cell_value(56,4))
                            if steps1_third_level_check:
                                steps1_third_level_save = ThirdLevelContent.objects.filter(second_level=steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,2), f1_1st_f2_text=worksheet.cell_value(44,3), f1_1st_f3_text=worksheet.cell_value(44,4), f1_2nd_f1_text=worksheet.cell_value(45,2), f1_2nd_f2_text=worksheet.cell_value(45,3), f1_2nd_f3_text=worksheet.cell_value(45,4), f1_3rd_f1_text=worksheet.cell_value(46,2), f1_3rd_f2_text=worksheet.cell_value(46,3), f1_3rd_f3_text=worksheet.cell_value(46,4), f2_1st_f1_text=worksheet.cell_value(49,2), f2_1st_f2_text=worksheet.cell_value(49,3), f2_1st_f3_text=worksheet.cell_value(49,4), f2_2nd_f1_text=worksheet.cell_value(50,2), f2_2nd_f2_text=worksheet.cell_value(50,3), f2_2nd_f3_text=worksheet.cell_value(50,4), f2_3rd_f1_text=worksheet.cell_value(51,2), f2_3rd_f2_text=worksheet.cell_value(51,3), f2_3rd_f3_text=worksheet.cell_value(51,4), f3_1st_f1_text=worksheet.cell_value(54,2), f3_1st_f2_text=worksheet.cell_value(54,3), f3_1st_f3_text=worksheet.cell_value(54,4), f3_2nd_f1_text=worksheet.cell_value(55,2), f3_2nd_f2_text=worksheet.cell_value(55,3), f3_2nd_f3_text=worksheet.cell_value(55,4), f3_3rd_f1_text=worksheet.cell_value(56,2), f3_3rd_f2_text=worksheet.cell_value(56,3), f3_3rd_f3_text=worksheet.cell_value(56,4))[0]
                            else:
                                steps1_third_level_save = ThirdLevelContent.objects.create(second_level=steps1_second_level_save, f1_1st_f1_text=worksheet.cell_value(44,2), f1_1st_f2_text=worksheet.cell_value(44,3), f1_1st_f3_text=worksheet.cell_value(44,4), f1_2nd_f1_text=worksheet.cell_value(45,2), f1_2nd_f2_text=worksheet.cell_value(45,3), f1_2nd_f3_text=worksheet.cell_value(45,4), f1_3rd_f1_text=worksheet.cell_value(46,2), f1_3rd_f2_text=worksheet.cell_value(46,3), f1_3rd_f3_text=worksheet.cell_value(46,4), f2_1st_f1_text=worksheet.cell_value(49,2), f2_1st_f2_text=worksheet.cell_value(49,3), f2_1st_f3_text=worksheet.cell_value(49,4), f2_2nd_f1_text=worksheet.cell_value(50,2), f2_2nd_f2_text=worksheet.cell_value(50,3), f2_2nd_f3_text=worksheet.cell_value(50,4), f2_3rd_f1_text=worksheet.cell_value(51,2), f2_3rd_f2_text=worksheet.cell_value(51,3), f2_3rd_f3_text=worksheet.cell_value(51,4), f3_1st_f1_text=worksheet.cell_value(54,2), f3_1st_f2_text=worksheet.cell_value(54,3), f3_1st_f3_text=worksheet.cell_value(54,4), f3_2nd_f1_text=worksheet.cell_value(55,2), f3_2nd_f2_text=worksheet.cell_value(55,3), f3_2nd_f3_text=worksheet.cell_value(55,4), f3_3rd_f1_text=worksheet.cell_value(56,2), f3_3rd_f2_text=worksheet.cell_value(56,3), f3_3rd_f3_text=worksheet.cell_value(56,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Steps Third Level values")
                        
                        try:
                            steps2_third_level_check = ThirdLevelContent.objects.filter(second_level=steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,2), f1_1st_f2_text=worksheet.cell_value(60,3), f1_1st_f3_text=worksheet.cell_value(60,4), f1_2nd_f1_text=worksheet.cell_value(61,2), f1_2nd_f2_text=worksheet.cell_value(61,3), f1_2nd_f3_text=worksheet.cell_value(61,4), f1_3rd_f1_text=worksheet.cell_value(62,2), f1_3rd_f2_text=worksheet.cell_value(62,3), f1_3rd_f3_text=worksheet.cell_value(62,4), f2_1st_f1_text=worksheet.cell_value(65,2), f2_1st_f2_text=worksheet.cell_value(65,3), f2_1st_f3_text=worksheet.cell_value(65,4), f2_2nd_f1_text=worksheet.cell_value(66,2), f2_2nd_f2_text=worksheet.cell_value(66,3), f2_2nd_f3_text=worksheet.cell_value(66,4), f2_3rd_f1_text=worksheet.cell_value(67,2), f2_3rd_f2_text=worksheet.cell_value(67,3), f2_3rd_f3_text=worksheet.cell_value(67,4), f3_1st_f1_text=worksheet.cell_value(70,2), f3_1st_f2_text=worksheet.cell_value(70,3), f3_1st_f3_text=worksheet.cell_value(70,4), f3_2nd_f1_text=worksheet.cell_value(71,2), f3_2nd_f2_text=worksheet.cell_value(71,3), f3_2nd_f3_text=worksheet.cell_value(71,4), f3_3rd_f1_text=worksheet.cell_value(72,2), f3_3rd_f2_text=worksheet.cell_value(72,3), f3_3rd_f3_text=worksheet.cell_value(72,4))
                            if steps2_third_level_check:
                                steps2_third_level_save = ThirdLevelContent.objects.filter(second_level=steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,2), f1_1st_f2_text=worksheet.cell_value(60,3), f1_1st_f3_text=worksheet.cell_value(60,4), f1_2nd_f1_text=worksheet.cell_value(61,2), f1_2nd_f2_text=worksheet.cell_value(61,3), f1_2nd_f3_text=worksheet.cell_value(61,4), f1_3rd_f1_text=worksheet.cell_value(62,2), f1_3rd_f2_text=worksheet.cell_value(62,3), f1_3rd_f3_text=worksheet.cell_value(62,4), f2_1st_f1_text=worksheet.cell_value(65,2), f2_1st_f2_text=worksheet.cell_value(65,3), f2_1st_f3_text=worksheet.cell_value(65,4), f2_2nd_f1_text=worksheet.cell_value(66,2), f2_2nd_f2_text=worksheet.cell_value(66,3), f2_2nd_f3_text=worksheet.cell_value(66,4), f2_3rd_f1_text=worksheet.cell_value(67,2), f2_3rd_f2_text=worksheet.cell_value(67,3), f2_3rd_f3_text=worksheet.cell_value(67,4), f3_1st_f1_text=worksheet.cell_value(70,2), f3_1st_f2_text=worksheet.cell_value(70,3), f3_1st_f3_text=worksheet.cell_value(70,4), f3_2nd_f1_text=worksheet.cell_value(71,2), f3_2nd_f2_text=worksheet.cell_value(71,3), f3_2nd_f3_text=worksheet.cell_value(71,4), f3_3rd_f1_text=worksheet.cell_value(72,2), f3_3rd_f2_text=worksheet.cell_value(72,3), f3_3rd_f3_text=worksheet.cell_value(72,4))[0]
                            else:
                                steps2_third_level_save = ThirdLevelContent.objects.create(second_level=steps2_second_level_save, f1_1st_f1_text=worksheet.cell_value(60,2), f1_1st_f2_text=worksheet.cell_value(60,3), f1_1st_f3_text=worksheet.cell_value(60,4), f1_2nd_f1_text=worksheet.cell_value(61,2), f1_2nd_f2_text=worksheet.cell_value(61,3), f1_2nd_f3_text=worksheet.cell_value(61,4), f1_3rd_f1_text=worksheet.cell_value(62,2), f1_3rd_f2_text=worksheet.cell_value(62,3), f1_3rd_f3_text=worksheet.cell_value(62,4), f2_1st_f1_text=worksheet.cell_value(65,2), f2_1st_f2_text=worksheet.cell_value(65,3), f2_1st_f3_text=worksheet.cell_value(65,4), f2_2nd_f1_text=worksheet.cell_value(66,2), f2_2nd_f2_text=worksheet.cell_value(66,3), f2_2nd_f3_text=worksheet.cell_value(66,4), f2_3rd_f1_text=worksheet.cell_value(67,2), f2_3rd_f2_text=worksheet.cell_value(67,3), f2_3rd_f3_text=worksheet.cell_value(67,4), f3_1st_f1_text=worksheet.cell_value(70,2), f3_1st_f2_text=worksheet.cell_value(70,3), f3_1st_f3_text=worksheet.cell_value(70,4), f3_2nd_f1_text=worksheet.cell_value(71,2), f3_2nd_f2_text=worksheet.cell_value(71,3), f3_2nd_f3_text=worksheet.cell_value(71,4), f3_3rd_f1_text=worksheet.cell_value(72,2), f3_3rd_f2_text=worksheet.cell_value(72,3), f3_3rd_f3_text=worksheet.cell_value(72,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Steps Third Level values")
                        
                        try:
                            weak1_third_level_check = ThirdLevelContent.objects.filter(second_level=weak1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,2), f1_1st_f2_text=worksheet.cell_value(78,3), f1_1st_f3_text=worksheet.cell_value(78,4), f1_2nd_f1_text=worksheet.cell_value(79,2), f1_2nd_f2_text=worksheet.cell_value(79,3), f1_2nd_f3_text=worksheet.cell_value(79,4), f1_3rd_f1_text=worksheet.cell_value(80,2), f1_3rd_f2_text=worksheet.cell_value(80,3), f1_3rd_f3_text=worksheet.cell_value(80,4), f2_1st_f1_text=worksheet.cell_value(83,2), f2_1st_f2_text=worksheet.cell_value(83,3), f2_1st_f3_text=worksheet.cell_value(83,4), f2_2nd_f1_text=worksheet.cell_value(84,2), f2_2nd_f2_text=worksheet.cell_value(84,3), f2_2nd_f3_text=worksheet.cell_value(84,4), f2_3rd_f1_text=worksheet.cell_value(85,2), f2_3rd_f2_text=worksheet.cell_value(85,3), f2_3rd_f3_text=worksheet.cell_value(85,4), f3_1st_f1_text=worksheet.cell_value(88,2), f3_1st_f2_text=worksheet.cell_value(88,3), f3_1st_f3_text=worksheet.cell_value(88,4), f3_2nd_f1_text=worksheet.cell_value(89,2), f3_2nd_f2_text=worksheet.cell_value(89,3), f3_2nd_f3_text=worksheet.cell_value(89,4), f3_3rd_f1_text=worksheet.cell_value(90,2), f3_3rd_f2_text=worksheet.cell_value(90,3), f3_3rd_f3_text=worksheet.cell_value(90,4))
                            if weak1_third_level_check:
                                weak1_third_level_save = ThirdLevelContent.objects.filter(second_level=weak1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,2), f1_1st_f2_text=worksheet.cell_value(78,3), f1_1st_f3_text=worksheet.cell_value(78,4), f1_2nd_f1_text=worksheet.cell_value(79,2), f1_2nd_f2_text=worksheet.cell_value(79,3), f1_2nd_f3_text=worksheet.cell_value(79,4), f1_3rd_f1_text=worksheet.cell_value(80,2), f1_3rd_f2_text=worksheet.cell_value(80,3), f1_3rd_f3_text=worksheet.cell_value(80,4), f2_1st_f1_text=worksheet.cell_value(83,2), f2_1st_f2_text=worksheet.cell_value(83,3), f2_1st_f3_text=worksheet.cell_value(83,4), f2_2nd_f1_text=worksheet.cell_value(84,2), f2_2nd_f2_text=worksheet.cell_value(84,3), f2_2nd_f3_text=worksheet.cell_value(84,4), f2_3rd_f1_text=worksheet.cell_value(85,2), f2_3rd_f2_text=worksheet.cell_value(85,3), f2_3rd_f3_text=worksheet.cell_value(85,4), f3_1st_f1_text=worksheet.cell_value(88,2), f3_1st_f2_text=worksheet.cell_value(88,3), f3_1st_f3_text=worksheet.cell_value(88,4), f3_2nd_f1_text=worksheet.cell_value(89,2), f3_2nd_f2_text=worksheet.cell_value(89,3), f3_2nd_f3_text=worksheet.cell_value(89,4), f3_3rd_f1_text=worksheet.cell_value(90,2), f3_3rd_f2_text=worksheet.cell_value(90,3), f3_3rd_f3_text=worksheet.cell_value(90,4))[0]
                            else:
                                weak1_third_level_save = ThirdLevelContent.objects.create(second_level=weak1_second_level_save, f1_1st_f1_text=worksheet.cell_value(78,2), f1_1st_f2_text=worksheet.cell_value(78,3), f1_1st_f3_text=worksheet.cell_value(78,4), f1_2nd_f1_text=worksheet.cell_value(79,2), f1_2nd_f2_text=worksheet.cell_value(79,3), f1_2nd_f3_text=worksheet.cell_value(79,4), f1_3rd_f1_text=worksheet.cell_value(80,2), f1_3rd_f2_text=worksheet.cell_value(80,3), f1_3rd_f3_text=worksheet.cell_value(80,4), f2_1st_f1_text=worksheet.cell_value(83,2), f2_1st_f2_text=worksheet.cell_value(83,3), f2_1st_f3_text=worksheet.cell_value(83,4), f2_2nd_f1_text=worksheet.cell_value(84,2), f2_2nd_f2_text=worksheet.cell_value(84,3), f2_2nd_f3_text=worksheet.cell_value(84,4), f2_3rd_f1_text=worksheet.cell_value(85,2), f2_3rd_f2_text=worksheet.cell_value(85,3), f2_3rd_f3_text=worksheet.cell_value(85,4), f3_1st_f1_text=worksheet.cell_value(88,2), f3_1st_f2_text=worksheet.cell_value(88,3), f3_1st_f3_text=worksheet.cell_value(88,4), f3_2nd_f1_text=worksheet.cell_value(89,2), f3_2nd_f2_text=worksheet.cell_value(89,3), f3_2nd_f3_text=worksheet.cell_value(89,4), f3_3rd_f1_text=worksheet.cell_value(90,2), f3_3rd_f2_text=worksheet.cell_value(90,3), f3_3rd_f3_text=worksheet.cell_value(90,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Weak Third Level values")
                        
                        try:
                            weak2_third_level_check = ThirdLevelContent.objects.filter(second_level=weak2_second_level_save, f1_1st_f1_text=worksheet.cell_value(94,2), f1_1st_f2_text=worksheet.cell_value(94,3), f1_1st_f3_text=worksheet.cell_value(94,4), f1_2nd_f1_text=worksheet.cell_value(95,2), f1_2nd_f2_text=worksheet.cell_value(95,3), f1_2nd_f3_text=worksheet.cell_value(95,4), f1_3rd_f1_text=worksheet.cell_value(96,2), f1_3rd_f2_text=worksheet.cell_value(96,3), f1_3rd_f3_text=worksheet.cell_value(96,4), f2_1st_f1_text=worksheet.cell_value(99,2), f2_1st_f2_text=worksheet.cell_value(99,3), f2_1st_f3_text=worksheet.cell_value(99,4), f2_2nd_f1_text=worksheet.cell_value(100,2), f2_2nd_f2_text=worksheet.cell_value(100,3), f2_2nd_f3_text=worksheet.cell_value(100,4), f2_3rd_f1_text=worksheet.cell_value(101,2), f2_3rd_f2_text=worksheet.cell_value(101,3), f2_3rd_f3_text=worksheet.cell_value(101,4), f3_1st_f1_text=worksheet.cell_value(104,2), f3_1st_f2_text=worksheet.cell_value(104,3), f3_1st_f3_text=worksheet.cell_value(104,4), f3_2nd_f1_text=worksheet.cell_value(105,2), f3_2nd_f2_text=worksheet.cell_value(105,3), f3_2nd_f3_text=worksheet.cell_value(105,4), f3_3rd_f1_text=worksheet.cell_value(106,2), f3_3rd_f2_text=worksheet.cell_value(106,3), f3_3rd_f3_text=worksheet.cell_value(106,4))
                            if weak2_third_level_check:
                                weak2_third_level_save = ThirdLevelContent.objects.filter(second_level=weak2_second_level_save, f1_1st_f1_text=worksheet.cell_value(94,2), f1_1st_f2_text=worksheet.cell_value(94,3), f1_1st_f3_text=worksheet.cell_value(94,4), f1_2nd_f1_text=worksheet.cell_value(95,2), f1_2nd_f2_text=worksheet.cell_value(95,3), f1_2nd_f3_text=worksheet.cell_value(95,4), f1_3rd_f1_text=worksheet.cell_value(96,2), f1_3rd_f2_text=worksheet.cell_value(96,3), f1_3rd_f3_text=worksheet.cell_value(96,4), f2_1st_f1_text=worksheet.cell_value(99,2), f2_1st_f2_text=worksheet.cell_value(99,3), f2_1st_f3_text=worksheet.cell_value(99,4), f2_2nd_f1_text=worksheet.cell_value(100,2), f2_2nd_f2_text=worksheet.cell_value(100,3), f2_2nd_f3_text=worksheet.cell_value(100,4), f2_3rd_f1_text=worksheet.cell_value(101,2), f2_3rd_f2_text=worksheet.cell_value(101,3), f2_3rd_f3_text=worksheet.cell_value(101,4), f3_1st_f1_text=worksheet.cell_value(104,2), f3_1st_f2_text=worksheet.cell_value(104,3), f3_1st_f3_text=worksheet.cell_value(104,4), f3_2nd_f1_text=worksheet.cell_value(105,2), f3_2nd_f2_text=worksheet.cell_value(105,3), f3_2nd_f3_text=worksheet.cell_value(105,4), f3_3rd_f1_text=worksheet.cell_value(106,2), f3_3rd_f2_text=worksheet.cell_value(106,3), f3_3rd_f3_text=worksheet.cell_value(106,4))[0]
                            else:
                                weak2_third_level_save = ThirdLevelContent.objects.create(second_level=weak2_second_level_save, f1_1st_f1_text=worksheet.cell_value(94,2), f1_1st_f2_text=worksheet.cell_value(94,3), f1_1st_f3_text=worksheet.cell_value(94,4), f1_2nd_f1_text=worksheet.cell_value(95,2), f1_2nd_f2_text=worksheet.cell_value(95,3), f1_2nd_f3_text=worksheet.cell_value(95,4), f1_3rd_f1_text=worksheet.cell_value(96,2), f1_3rd_f2_text=worksheet.cell_value(96,3), f1_3rd_f3_text=worksheet.cell_value(96,4), f2_1st_f1_text=worksheet.cell_value(99,2), f2_1st_f2_text=worksheet.cell_value(99,3), f2_1st_f3_text=worksheet.cell_value(99,4), f2_2nd_f1_text=worksheet.cell_value(100,2), f2_2nd_f2_text=worksheet.cell_value(100,3), f2_2nd_f3_text=worksheet.cell_value(100,4), f2_3rd_f1_text=worksheet.cell_value(101,2), f2_3rd_f2_text=worksheet.cell_value(101,3), f2_3rd_f3_text=worksheet.cell_value(101,4), f3_1st_f1_text=worksheet.cell_value(104,2), f3_1st_f2_text=worksheet.cell_value(104,3), f3_1st_f3_text=worksheet.cell_value(104,4), f3_2nd_f1_text=worksheet.cell_value(105,2), f3_2nd_f2_text=worksheet.cell_value(105,3), f3_2nd_f3_text=worksheet.cell_value(105,4), f3_3rd_f1_text=worksheet.cell_value(106,2), f3_3rd_f2_text=worksheet.cell_value(106,3), f3_3rd_f3_text=worksheet.cell_value(106,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Weak Third Level values")
                        
                        try:
                            low1_third_level_check = ThirdLevelContent.objects.filter(second_level=low1_second_level_save, f1_1st_f1_text=worksheet.cell_value(112,2), f1_1st_f2_text=worksheet.cell_value(112,3), f1_1st_f3_text=worksheet.cell_value(112,4), f1_2nd_f1_text=worksheet.cell_value(113,2), f1_2nd_f2_text=worksheet.cell_value(113,3), f1_2nd_f3_text=worksheet.cell_value(113,4), f1_3rd_f1_text=worksheet.cell_value(114,2), f1_3rd_f2_text=worksheet.cell_value(114,3), f1_3rd_f3_text=worksheet.cell_value(114,4), f2_1st_f1_text=worksheet.cell_value(117,2), f2_1st_f2_text=worksheet.cell_value(117,3), f2_1st_f3_text=worksheet.cell_value(117,4), f2_2nd_f1_text=worksheet.cell_value(118,2), f2_2nd_f2_text=worksheet.cell_value(118,3), f2_2nd_f3_text=worksheet.cell_value(118,4), f2_3rd_f1_text=worksheet.cell_value(119,2), f2_3rd_f2_text=worksheet.cell_value(119,3), f2_3rd_f3_text=worksheet.cell_value(119,4), f3_1st_f1_text=worksheet.cell_value(122,2), f3_1st_f2_text=worksheet.cell_value(122,3), f3_1st_f3_text=worksheet.cell_value(122,4), f3_2nd_f1_text=worksheet.cell_value(123,2), f3_2nd_f2_text=worksheet.cell_value(123,3), f3_2nd_f3_text=worksheet.cell_value(123,4), f3_3rd_f1_text=worksheet.cell_value(124,2), f3_3rd_f2_text=worksheet.cell_value(124,3), f3_3rd_f3_text=worksheet.cell_value(124,4))
                            if low1_third_level_check:
                                low1_third_level_save = ThirdLevelContent.objects.filter(second_level=low1_second_level_save, f1_1st_f1_text=worksheet.cell_value(112,2), f1_1st_f2_text=worksheet.cell_value(112,3), f1_1st_f3_text=worksheet.cell_value(112,4), f1_2nd_f1_text=worksheet.cell_value(113,2), f1_2nd_f2_text=worksheet.cell_value(113,3), f1_2nd_f3_text=worksheet.cell_value(113,4), f1_3rd_f1_text=worksheet.cell_value(114,2), f1_3rd_f2_text=worksheet.cell_value(114,3), f1_3rd_f3_text=worksheet.cell_value(114,4), f2_1st_f1_text=worksheet.cell_value(117,2), f2_1st_f2_text=worksheet.cell_value(117,3), f2_1st_f3_text=worksheet.cell_value(117,4), f2_2nd_f1_text=worksheet.cell_value(118,2), f2_2nd_f2_text=worksheet.cell_value(118,3), f2_2nd_f3_text=worksheet.cell_value(118,4), f2_3rd_f1_text=worksheet.cell_value(119,2), f2_3rd_f2_text=worksheet.cell_value(119,3), f2_3rd_f3_text=worksheet.cell_value(119,4), f3_1st_f1_text=worksheet.cell_value(122,2), f3_1st_f2_text=worksheet.cell_value(122,3), f3_1st_f3_text=worksheet.cell_value(122,4), f3_2nd_f1_text=worksheet.cell_value(123,2), f3_2nd_f2_text=worksheet.cell_value(123,3), f3_2nd_f3_text=worksheet.cell_value(123,4), f3_3rd_f1_text=worksheet.cell_value(124,2), f3_3rd_f2_text=worksheet.cell_value(124,3), f3_3rd_f3_text=worksheet.cell_value(124,4))[0]
                            else:
                                low1_third_level_save = ThirdLevelContent.objects.create(second_level=low1_second_level_save, f1_1st_f1_text=worksheet.cell_value(112,2), f1_1st_f2_text=worksheet.cell_value(112,3), f1_1st_f3_text=worksheet.cell_value(112,4), f1_2nd_f1_text=worksheet.cell_value(113,2), f1_2nd_f2_text=worksheet.cell_value(113,3), f1_2nd_f3_text=worksheet.cell_value(113,4), f1_3rd_f1_text=worksheet.cell_value(114,2), f1_3rd_f2_text=worksheet.cell_value(114,3), f1_3rd_f3_text=worksheet.cell_value(114,4), f2_1st_f1_text=worksheet.cell_value(117,2), f2_1st_f2_text=worksheet.cell_value(117,3), f2_1st_f3_text=worksheet.cell_value(117,4), f2_2nd_f1_text=worksheet.cell_value(118,2), f2_2nd_f2_text=worksheet.cell_value(118,3), f2_2nd_f3_text=worksheet.cell_value(118,4), f2_3rd_f1_text=worksheet.cell_value(119,2), f2_3rd_f2_text=worksheet.cell_value(119,3), f2_3rd_f3_text=worksheet.cell_value(119,4), f3_1st_f1_text=worksheet.cell_value(122,2), f3_1st_f2_text=worksheet.cell_value(122,3), f3_1st_f3_text=worksheet.cell_value(122,4), f3_2nd_f1_text=worksheet.cell_value(123,2), f3_2nd_f2_text=worksheet.cell_value(123,3), f3_2nd_f3_text=worksheet.cell_value(123,4), f3_3rd_f1_text=worksheet.cell_value(124,2), f3_3rd_f2_text=worksheet.cell_value(124,3), f3_3rd_f3_text=worksheet.cell_value(124,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Low Third Level values")
                        
                        try:
                            low2_third_level_check = ThirdLevelContent.objects.filter(second_level=low2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,2), f1_1st_f2_text=worksheet.cell_value(128,3), f1_1st_f3_text=worksheet.cell_value(128,4), f1_2nd_f1_text=worksheet.cell_value(129,2), f1_2nd_f2_text=worksheet.cell_value(129,3), f1_2nd_f3_text=worksheet.cell_value(129,4), f1_3rd_f1_text=worksheet.cell_value(130,2), f1_3rd_f2_text=worksheet.cell_value(130,3), f1_3rd_f3_text=worksheet.cell_value(130,4), f2_1st_f1_text=worksheet.cell_value(133,2), f2_1st_f2_text=worksheet.cell_value(133,3), f2_1st_f3_text=worksheet.cell_value(133,4), f2_2nd_f1_text=worksheet.cell_value(134,2), f2_2nd_f2_text=worksheet.cell_value(134,3), f2_2nd_f3_text=worksheet.cell_value(134,4), f2_3rd_f1_text=worksheet.cell_value(135,2), f2_3rd_f2_text=worksheet.cell_value(135,3), f2_3rd_f3_text=worksheet.cell_value(135,4), f3_1st_f1_text=worksheet.cell_value(138,2), f3_1st_f2_text=worksheet.cell_value(138,3), f3_1st_f3_text=worksheet.cell_value(138,4), f3_2nd_f1_text=worksheet.cell_value(139,2), f3_2nd_f2_text=worksheet.cell_value(139,3), f3_2nd_f3_text=worksheet.cell_value(139,4), f3_3rd_f1_text=worksheet.cell_value(140,2), f3_3rd_f2_text=worksheet.cell_value(140,3), f3_3rd_f3_text=worksheet.cell_value(140,4))
                            if low2_third_level_check:
                                low2_third_level_save = ThirdLevelContent.objects.filter(second_level=low2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,2), f1_1st_f2_text=worksheet.cell_value(128,3), f1_1st_f3_text=worksheet.cell_value(128,4), f1_2nd_f1_text=worksheet.cell_value(129,2), f1_2nd_f2_text=worksheet.cell_value(129,3), f1_2nd_f3_text=worksheet.cell_value(129,4), f1_3rd_f1_text=worksheet.cell_value(130,2), f1_3rd_f2_text=worksheet.cell_value(130,3), f1_3rd_f3_text=worksheet.cell_value(130,4), f2_1st_f1_text=worksheet.cell_value(133,2), f2_1st_f2_text=worksheet.cell_value(133,3), f2_1st_f3_text=worksheet.cell_value(133,4), f2_2nd_f1_text=worksheet.cell_value(134,2), f2_2nd_f2_text=worksheet.cell_value(134,3), f2_2nd_f3_text=worksheet.cell_value(134,4), f2_3rd_f1_text=worksheet.cell_value(135,2), f2_3rd_f2_text=worksheet.cell_value(135,3), f2_3rd_f3_text=worksheet.cell_value(135,4), f3_1st_f1_text=worksheet.cell_value(138,2), f3_1st_f2_text=worksheet.cell_value(138,3), f3_1st_f3_text=worksheet.cell_value(138,4), f3_2nd_f1_text=worksheet.cell_value(139,2), f3_2nd_f2_text=worksheet.cell_value(139,3), f3_2nd_f3_text=worksheet.cell_value(139,4), f3_3rd_f1_text=worksheet.cell_value(140,2), f3_3rd_f2_text=worksheet.cell_value(140,3), f3_3rd_f3_text=worksheet.cell_value(140,4))[0]
                            else:
                                low2_third_level_save = ThirdLevelContent.objects.create(second_level=low2_second_level_save, f1_1st_f1_text=worksheet.cell_value(128,2), f1_1st_f2_text=worksheet.cell_value(128,3), f1_1st_f3_text=worksheet.cell_value(128,4), f1_2nd_f1_text=worksheet.cell_value(129,2), f1_2nd_f2_text=worksheet.cell_value(129,3), f1_2nd_f3_text=worksheet.cell_value(129,4), f1_3rd_f1_text=worksheet.cell_value(130,2), f1_3rd_f2_text=worksheet.cell_value(130,3), f1_3rd_f3_text=worksheet.cell_value(130,4), f2_1st_f1_text=worksheet.cell_value(133,2), f2_1st_f2_text=worksheet.cell_value(133,3), f2_1st_f3_text=worksheet.cell_value(133,4), f2_2nd_f1_text=worksheet.cell_value(134,2), f2_2nd_f2_text=worksheet.cell_value(134,3), f2_2nd_f3_text=worksheet.cell_value(134,4), f2_3rd_f1_text=worksheet.cell_value(135,2), f2_3rd_f2_text=worksheet.cell_value(135,3), f2_3rd_f3_text=worksheet.cell_value(135,4), f3_1st_f1_text=worksheet.cell_value(138,2), f3_1st_f2_text=worksheet.cell_value(138,3), f3_1st_f3_text=worksheet.cell_value(138,4), f3_2nd_f1_text=worksheet.cell_value(139,2), f3_2nd_f2_text=worksheet.cell_value(139,3), f3_2nd_f3_text=worksheet.cell_value(139,4), f3_3rd_f1_text=worksheet.cell_value(140,2), f3_3rd_f2_text=worksheet.cell_value(140,3), f3_3rd_f3_text=worksheet.cell_value(140,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Low Third Level values")
                        
                        try:
                            current1_third_level_check = ThirdLevelContent.objects.filter(second_level=current1_second_level_save, f1_1st_f1_text=worksheet.cell_value(146,2), f1_1st_f2_text=worksheet.cell_value(146,3), f1_1st_f3_text=worksheet.cell_value(146,4), f1_2nd_f1_text=worksheet.cell_value(147,2), f1_2nd_f2_text=worksheet.cell_value(147,3), f1_2nd_f3_text=worksheet.cell_value(147,4), f1_3rd_f1_text=worksheet.cell_value(148,2), f1_3rd_f2_text=worksheet.cell_value(148,3), f1_3rd_f3_text=worksheet.cell_value(148,4), f2_1st_f1_text=worksheet.cell_value(151,2), f2_1st_f2_text=worksheet.cell_value(151,3), f2_1st_f3_text=worksheet.cell_value(151,4), f2_2nd_f1_text=worksheet.cell_value(152,2), f2_2nd_f2_text=worksheet.cell_value(152,3), f2_2nd_f3_text=worksheet.cell_value(152,4), f2_3rd_f1_text=worksheet.cell_value(153,2), f2_3rd_f2_text=worksheet.cell_value(153,3), f2_3rd_f3_text=worksheet.cell_value(153,4), f3_1st_f1_text=worksheet.cell_value(156,2), f3_1st_f2_text=worksheet.cell_value(156,3), f3_1st_f3_text=worksheet.cell_value(156,4), f3_2nd_f1_text=worksheet.cell_value(157,2), f3_2nd_f2_text=worksheet.cell_value(157,3), f3_2nd_f3_text=worksheet.cell_value(157,4), f3_3rd_f1_text=worksheet.cell_value(158,2), f3_3rd_f2_text=worksheet.cell_value(158,3), f3_3rd_f3_text=worksheet.cell_value(158,4))
                            if current1_third_level_check:
                                current1_third_level_save = ThirdLevelContent.objects.filter(second_level=current1_second_level_save, f1_1st_f1_text=worksheet.cell_value(146,2), f1_1st_f2_text=worksheet.cell_value(146,3), f1_1st_f3_text=worksheet.cell_value(146,4), f1_2nd_f1_text=worksheet.cell_value(147,2), f1_2nd_f2_text=worksheet.cell_value(147,3), f1_2nd_f3_text=worksheet.cell_value(147,4), f1_3rd_f1_text=worksheet.cell_value(148,2), f1_3rd_f2_text=worksheet.cell_value(148,3), f1_3rd_f3_text=worksheet.cell_value(148,4), f2_1st_f1_text=worksheet.cell_value(151,2), f2_1st_f2_text=worksheet.cell_value(151,3), f2_1st_f3_text=worksheet.cell_value(151,4), f2_2nd_f1_text=worksheet.cell_value(152,2), f2_2nd_f2_text=worksheet.cell_value(152,3), f2_2nd_f3_text=worksheet.cell_value(152,4), f2_3rd_f1_text=worksheet.cell_value(153,2), f2_3rd_f2_text=worksheet.cell_value(153,3), f2_3rd_f3_text=worksheet.cell_value(153,4), f3_1st_f1_text=worksheet.cell_value(156,2), f3_1st_f2_text=worksheet.cell_value(156,3), f3_1st_f3_text=worksheet.cell_value(156,4), f3_2nd_f1_text=worksheet.cell_value(157,2), f3_2nd_f2_text=worksheet.cell_value(157,3), f3_2nd_f3_text=worksheet.cell_value(157,4), f3_3rd_f1_text=worksheet.cell_value(158,2), f3_3rd_f2_text=worksheet.cell_value(158,3), f3_3rd_f3_text=worksheet.cell_value(158,4))[0]
                            else:
                                current1_third_level_save = ThirdLevelContent.objects.create(second_level=current1_second_level_save, f1_1st_f1_text=worksheet.cell_value(146,2), f1_1st_f2_text=worksheet.cell_value(146,3), f1_1st_f3_text=worksheet.cell_value(146,4), f1_2nd_f1_text=worksheet.cell_value(147,2), f1_2nd_f2_text=worksheet.cell_value(147,3), f1_2nd_f3_text=worksheet.cell_value(147,4), f1_3rd_f1_text=worksheet.cell_value(148,2), f1_3rd_f2_text=worksheet.cell_value(148,3), f1_3rd_f3_text=worksheet.cell_value(148,4), f2_1st_f1_text=worksheet.cell_value(151,2), f2_1st_f2_text=worksheet.cell_value(151,3), f2_1st_f3_text=worksheet.cell_value(151,4), f2_2nd_f1_text=worksheet.cell_value(152,2), f2_2nd_f2_text=worksheet.cell_value(152,3), f2_2nd_f3_text=worksheet.cell_value(152,4), f2_3rd_f1_text=worksheet.cell_value(153,2), f2_3rd_f2_text=worksheet.cell_value(153,3), f2_3rd_f3_text=worksheet.cell_value(153,4), f3_1st_f1_text=worksheet.cell_value(156,2), f3_1st_f2_text=worksheet.cell_value(156,3), f3_1st_f3_text=worksheet.cell_value(156,4), f3_2nd_f1_text=worksheet.cell_value(157,2), f3_2nd_f2_text=worksheet.cell_value(157,3), f3_2nd_f3_text=worksheet.cell_value(157,4), f3_3rd_f1_text=worksheet.cell_value(158,2), f3_3rd_f2_text=worksheet.cell_value(158,3), f3_3rd_f3_text=worksheet.cell_value(158,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Current Third Level values")
                        
                        try:
                            current2_third_level_check = ThirdLevelContent.objects.filter(second_level=current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,2), f1_1st_f2_text=worksheet.cell_value(162,3), f1_1st_f3_text=worksheet.cell_value(162,4), f1_2nd_f1_text=worksheet.cell_value(163,2), f1_2nd_f2_text=worksheet.cell_value(163,3), f1_2nd_f3_text=worksheet.cell_value(163,4), f1_3rd_f1_text=worksheet.cell_value(164,2), f1_3rd_f2_text=worksheet.cell_value(164,3), f1_3rd_f3_text=worksheet.cell_value(164,4), f2_1st_f1_text=worksheet.cell_value(167,2), f2_1st_f2_text=worksheet.cell_value(167,3), f2_1st_f3_text=worksheet.cell_value(167,4), f2_2nd_f1_text=worksheet.cell_value(168,2), f2_2nd_f2_text=worksheet.cell_value(168,3), f2_2nd_f3_text=worksheet.cell_value(168,4), f2_3rd_f1_text=worksheet.cell_value(169,2), f2_3rd_f2_text=worksheet.cell_value(169,3), f2_3rd_f3_text=worksheet.cell_value(169,4), f3_1st_f1_text=worksheet.cell_value(172,2), f3_1st_f2_text=worksheet.cell_value(172,3), f3_1st_f3_text=worksheet.cell_value(172,4), f3_2nd_f1_text=worksheet.cell_value(173,2), f3_2nd_f2_text=worksheet.cell_value(173,3), f3_2nd_f3_text=worksheet.cell_value(173,4), f3_3rd_f1_text=worksheet.cell_value(174,2), f3_3rd_f2_text=worksheet.cell_value(174,3), f3_3rd_f3_text=worksheet.cell_value(174,4))
                            if current2_third_level_check:
                                current2_third_level_save = ThirdLevelContent.objects.filter(second_level=current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,2), f1_1st_f2_text=worksheet.cell_value(162,3), f1_1st_f3_text=worksheet.cell_value(162,4), f1_2nd_f1_text=worksheet.cell_value(163,2), f1_2nd_f2_text=worksheet.cell_value(163,3), f1_2nd_f3_text=worksheet.cell_value(163,4), f1_3rd_f1_text=worksheet.cell_value(164,2), f1_3rd_f2_text=worksheet.cell_value(164,3), f1_3rd_f3_text=worksheet.cell_value(164,4), f2_1st_f1_text=worksheet.cell_value(167,2), f2_1st_f2_text=worksheet.cell_value(167,3), f2_1st_f3_text=worksheet.cell_value(167,4), f2_2nd_f1_text=worksheet.cell_value(168,2), f2_2nd_f2_text=worksheet.cell_value(168,3), f2_2nd_f3_text=worksheet.cell_value(168,4), f2_3rd_f1_text=worksheet.cell_value(169,2), f2_3rd_f2_text=worksheet.cell_value(169,3), f2_3rd_f3_text=worksheet.cell_value(169,4), f3_1st_f1_text=worksheet.cell_value(172,2), f3_1st_f2_text=worksheet.cell_value(172,3), f3_1st_f3_text=worksheet.cell_value(172,4), f3_2nd_f1_text=worksheet.cell_value(173,2), f3_2nd_f2_text=worksheet.cell_value(173,3), f3_2nd_f3_text=worksheet.cell_value(173,4), f3_3rd_f1_text=worksheet.cell_value(174,2), f3_3rd_f2_text=worksheet.cell_value(174,3), f3_3rd_f3_text=worksheet.cell_value(174,4))[0]
                            else:
                                current2_third_level_save = ThirdLevelContent.objects.create(second_level=current2_second_level_save, f1_1st_f1_text=worksheet.cell_value(162,2), f1_1st_f2_text=worksheet.cell_value(162,3), f1_1st_f3_text=worksheet.cell_value(162,4), f1_2nd_f1_text=worksheet.cell_value(163,2), f1_2nd_f2_text=worksheet.cell_value(163,3), f1_2nd_f3_text=worksheet.cell_value(163,4), f1_3rd_f1_text=worksheet.cell_value(164,2), f1_3rd_f2_text=worksheet.cell_value(164,3), f1_3rd_f3_text=worksheet.cell_value(164,4), f2_1st_f1_text=worksheet.cell_value(167,2), f2_1st_f2_text=worksheet.cell_value(167,3), f2_1st_f3_text=worksheet.cell_value(167,4), f2_2nd_f1_text=worksheet.cell_value(168,2), f2_2nd_f2_text=worksheet.cell_value(168,3), f2_2nd_f3_text=worksheet.cell_value(168,4), f2_3rd_f1_text=worksheet.cell_value(169,2), f2_3rd_f2_text=worksheet.cell_value(169,3), f2_3rd_f3_text=worksheet.cell_value(169,4), f3_1st_f1_text=worksheet.cell_value(172,2), f3_1st_f2_text=worksheet.cell_value(172,3), f3_1st_f3_text=worksheet.cell_value(172,4), f3_2nd_f1_text=worksheet.cell_value(173,2), f3_2nd_f2_text=worksheet.cell_value(173,3), f3_2nd_f3_text=worksheet.cell_value(173,4), f3_3rd_f1_text=worksheet.cell_value(174,2), f3_3rd_f2_text=worksheet.cell_value(174,3), f3_3rd_f3_text=worksheet.cell_value(174,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Current Third Level values")
                        
                        try:
                            habitats1_third_level_check = ThirdLevelContent.objects.filter(second_level=habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,2), f1_1st_f2_text=worksheet.cell_value(180,3), f1_1st_f3_text=worksheet.cell_value(180,4), f1_2nd_f1_text=worksheet.cell_value(181,2), f1_2nd_f2_text=worksheet.cell_value(181,3), f1_2nd_f3_text=worksheet.cell_value(181,4), f1_3rd_f1_text=worksheet.cell_value(182,2), f1_3rd_f2_text=worksheet.cell_value(182,3), f1_3rd_f3_text=worksheet.cell_value(182,4), f2_1st_f1_text=worksheet.cell_value(185,2), f2_1st_f2_text=worksheet.cell_value(185,3), f2_1st_f3_text=worksheet.cell_value(185,4), f2_2nd_f1_text=worksheet.cell_value(186,2), f2_2nd_f2_text=worksheet.cell_value(186,3), f2_2nd_f3_text=worksheet.cell_value(186,4), f2_3rd_f1_text=worksheet.cell_value(187,2), f2_3rd_f2_text=worksheet.cell_value(187,3), f2_3rd_f3_text=worksheet.cell_value(187,4), f3_1st_f1_text=worksheet.cell_value(190,2), f3_1st_f2_text=worksheet.cell_value(190,3), f3_1st_f3_text=worksheet.cell_value(190,4), f3_2nd_f1_text=worksheet.cell_value(191,2), f3_2nd_f2_text=worksheet.cell_value(191,3), f3_2nd_f3_text=worksheet.cell_value(191,4), f3_3rd_f1_text=worksheet.cell_value(192,2), f3_3rd_f2_text=worksheet.cell_value(192,3), f3_3rd_f3_text=worksheet.cell_value(192,4))
                            if habitats1_third_level_check:
                                habitats1_third_level_save = ThirdLevelContent.objects.filter(second_level=habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,2), f1_1st_f2_text=worksheet.cell_value(180,3), f1_1st_f3_text=worksheet.cell_value(180,4), f1_2nd_f1_text=worksheet.cell_value(181,2), f1_2nd_f2_text=worksheet.cell_value(181,3), f1_2nd_f3_text=worksheet.cell_value(181,4), f1_3rd_f1_text=worksheet.cell_value(182,2), f1_3rd_f2_text=worksheet.cell_value(182,3), f1_3rd_f3_text=worksheet.cell_value(182,4), f2_1st_f1_text=worksheet.cell_value(185,2), f2_1st_f2_text=worksheet.cell_value(185,3), f2_1st_f3_text=worksheet.cell_value(185,4), f2_2nd_f1_text=worksheet.cell_value(186,2), f2_2nd_f2_text=worksheet.cell_value(186,3), f2_2nd_f3_text=worksheet.cell_value(186,4), f2_3rd_f1_text=worksheet.cell_value(187,2), f2_3rd_f2_text=worksheet.cell_value(187,3), f2_3rd_f3_text=worksheet.cell_value(187,4), f3_1st_f1_text=worksheet.cell_value(190,2), f3_1st_f2_text=worksheet.cell_value(190,3), f3_1st_f3_text=worksheet.cell_value(190,4), f3_2nd_f1_text=worksheet.cell_value(191,2), f3_2nd_f2_text=worksheet.cell_value(191,3), f3_2nd_f3_text=worksheet.cell_value(191,4), f3_3rd_f1_text=worksheet.cell_value(192,2), f3_3rd_f2_text=worksheet.cell_value(192,3), f3_3rd_f3_text=worksheet.cell_value(192,4))[0]
                            else:
                                habitats1_third_level_save = ThirdLevelContent.objects.create(second_level=habitats1_second_level_save, f1_1st_f1_text=worksheet.cell_value(180,2), f1_1st_f2_text=worksheet.cell_value(180,3), f1_1st_f3_text=worksheet.cell_value(180,4), f1_2nd_f1_text=worksheet.cell_value(181,2), f1_2nd_f2_text=worksheet.cell_value(181,3), f1_2nd_f3_text=worksheet.cell_value(181,4), f1_3rd_f1_text=worksheet.cell_value(182,2), f1_3rd_f2_text=worksheet.cell_value(182,3), f1_3rd_f3_text=worksheet.cell_value(182,4), f2_1st_f1_text=worksheet.cell_value(185,2), f2_1st_f2_text=worksheet.cell_value(185,3), f2_1st_f3_text=worksheet.cell_value(185,4), f2_2nd_f1_text=worksheet.cell_value(186,2), f2_2nd_f2_text=worksheet.cell_value(186,3), f2_2nd_f3_text=worksheet.cell_value(186,4), f2_3rd_f1_text=worksheet.cell_value(187,2), f2_3rd_f2_text=worksheet.cell_value(187,3), f2_3rd_f3_text=worksheet.cell_value(187,4), f3_1st_f1_text=worksheet.cell_value(190,2), f3_1st_f2_text=worksheet.cell_value(190,3), f3_1st_f3_text=worksheet.cell_value(190,4), f3_2nd_f1_text=worksheet.cell_value(191,2), f3_2nd_f2_text=worksheet.cell_value(191,3), f3_2nd_f3_text=worksheet.cell_value(191,4), f3_3rd_f1_text=worksheet.cell_value(192,2), f3_3rd_f2_text=worksheet.cell_value(192,3), f3_3rd_f3_text=worksheet.cell_value(192,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" First Habitats Third Level values")
                        
                        try:
                            habitats2_third_level_check = ThirdLevelContent.objects.filter(second_level=habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,2), f1_1st_f2_text=worksheet.cell_value(196,3), f1_1st_f3_text=worksheet.cell_value(196,4), f1_2nd_f1_text=worksheet.cell_value(197,2), f1_2nd_f2_text=worksheet.cell_value(197,3), f1_2nd_f3_text=worksheet.cell_value(197,4), f1_3rd_f1_text=worksheet.cell_value(198,2), f1_3rd_f2_text=worksheet.cell_value(198,3), f1_3rd_f3_text=worksheet.cell_value(198,4), f2_1st_f1_text=worksheet.cell_value(201,2), f2_1st_f2_text=worksheet.cell_value(201,3), f2_1st_f3_text=worksheet.cell_value(201,4), f2_2nd_f1_text=worksheet.cell_value(202,2), f2_2nd_f2_text=worksheet.cell_value(202,3), f2_2nd_f3_text=worksheet.cell_value(202,4), f2_3rd_f1_text=worksheet.cell_value(203,2), f2_3rd_f2_text=worksheet.cell_value(203,3), f2_3rd_f3_text=worksheet.cell_value(203,4), f3_1st_f1_text=worksheet.cell_value(206,2), f3_1st_f2_text=worksheet.cell_value(206,3), f3_1st_f3_text=worksheet.cell_value(206,4), f3_2nd_f1_text=worksheet.cell_value(207,2), f3_2nd_f2_text=worksheet.cell_value(207,3), f3_2nd_f3_text=worksheet.cell_value(207,4), f3_3rd_f1_text=worksheet.cell_value(208,2), f3_3rd_f2_text=worksheet.cell_value(208,3), f3_3rd_f3_text=worksheet.cell_value(208,4))
                            if habitats2_third_level_check:
                                habitats2_third_level_save = ThirdLevelContent.objects.filter(second_level=habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,2), f1_1st_f2_text=worksheet.cell_value(196,3), f1_1st_f3_text=worksheet.cell_value(196,4), f1_2nd_f1_text=worksheet.cell_value(197,2), f1_2nd_f2_text=worksheet.cell_value(197,3), f1_2nd_f3_text=worksheet.cell_value(197,4), f1_3rd_f1_text=worksheet.cell_value(198,2), f1_3rd_f2_text=worksheet.cell_value(198,3), f1_3rd_f3_text=worksheet.cell_value(198,4), f2_1st_f1_text=worksheet.cell_value(201,2), f2_1st_f2_text=worksheet.cell_value(201,3), f2_1st_f3_text=worksheet.cell_value(201,4), f2_2nd_f1_text=worksheet.cell_value(202,2), f2_2nd_f2_text=worksheet.cell_value(202,3), f2_2nd_f3_text=worksheet.cell_value(202,4), f2_3rd_f1_text=worksheet.cell_value(203,2), f2_3rd_f2_text=worksheet.cell_value(203,3), f2_3rd_f3_text=worksheet.cell_value(203,4), f3_1st_f1_text=worksheet.cell_value(206,2), f3_1st_f2_text=worksheet.cell_value(206,3), f3_1st_f3_text=worksheet.cell_value(206,4), f3_2nd_f1_text=worksheet.cell_value(207,2), f3_2nd_f2_text=worksheet.cell_value(207,3), f3_2nd_f3_text=worksheet.cell_value(207,4), f3_3rd_f1_text=worksheet.cell_value(208,2), f3_3rd_f2_text=worksheet.cell_value(208,3), f3_3rd_f3_text=worksheet.cell_value(208,4))[0]
                            else:
                                habitats2_third_level_save = ThirdLevelContent.objects.create(second_level=habitats2_second_level_save, f1_1st_f1_text=worksheet.cell_value(196,2), f1_1st_f2_text=worksheet.cell_value(196,3), f1_1st_f3_text=worksheet.cell_value(196,4), f1_2nd_f1_text=worksheet.cell_value(197,2), f1_2nd_f2_text=worksheet.cell_value(197,3), f1_2nd_f3_text=worksheet.cell_value(197,4), f1_3rd_f1_text=worksheet.cell_value(198,2), f1_3rd_f2_text=worksheet.cell_value(198,3), f1_3rd_f3_text=worksheet.cell_value(198,4), f2_1st_f1_text=worksheet.cell_value(201,2), f2_1st_f2_text=worksheet.cell_value(201,3), f2_1st_f3_text=worksheet.cell_value(201,4), f2_2nd_f1_text=worksheet.cell_value(202,2), f2_2nd_f2_text=worksheet.cell_value(202,3), f2_2nd_f3_text=worksheet.cell_value(202,4), f2_3rd_f1_text=worksheet.cell_value(203,2), f2_3rd_f2_text=worksheet.cell_value(203,3), f2_3rd_f3_text=worksheet.cell_value(203,4), f3_1st_f1_text=worksheet.cell_value(206,2), f3_1st_f2_text=worksheet.cell_value(206,3), f3_1st_f3_text=worksheet.cell_value(206,4), f3_2nd_f1_text=worksheet.cell_value(207,2), f3_2nd_f2_text=worksheet.cell_value(207,3), f3_2nd_f3_text=worksheet.cell_value(207,4), f3_3rd_f1_text=worksheet.cell_value(208,2), f3_3rd_f2_text=worksheet.cell_value(208,3), f3_3rd_f3_text=worksheet.cell_value(208,4))
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" Second Habitats Third Level values")
                        
                        try:
                            current_reality_check = Current_Reality.objects.filter(name=worksheet.cell_value(2,1), category=category_save, subcategory=sub_category_save, related_want=want_save, negative_i_want_show_more_content_1=negative1_first_level_save, negative_i_want_show_more_content_2=negative2_first_level_save, steps_to_turn_negative_show_more_content_1=steps1_first_level_save, steps_to_turn_negative_show_more_content_2= steps2_first_level_save, weak_and_disgrace_show_more_content_1=weak1_first_level_save , weak_and_disgrace_show_more_content_2=weak2_first_level_save, low_performance_ability_show_more_content_1=low1_first_level_save, low_performance_ability_show_more_content_2=low2_first_level_save, current_habits_of_ability_show_more_content_1=current1_first_level_save, current_habits_of_ability_show_more_content_2=current2_first_level_save, habitats_outside_of_me_show_more_content_1=habitats1_first_level_save, habitats_outside_of_me_show_more_content_2=habitats2_first_level_save)
                            if current_reality_check:
                                check=True
                                warning.append(worksheet.cell_value(2,1)+ " current reality already exists")
                            if not current_reality_check:
                                if worksheet.cell_value(2,3)!= "":
                                    check=False
                                    current_reality_save=Current_Reality.objects.create(name=worksheet.cell_value(2,1), order=worksheet.cell_value(2,3), category=category_save, subcategory=sub_category_save, related_want=want_save, negative_i_want_show_more_content_1=negative1_first_level_save, negative_i_want_show_more_content_2=negative2_first_level_save, steps_to_turn_negative_show_more_content_1=steps1_first_level_save, steps_to_turn_negative_show_more_content_2= steps2_first_level_save, weak_and_disgrace_show_more_content_1=weak1_first_level_save , weak_and_disgrace_show_more_content_2=weak2_first_level_save, low_performance_ability_show_more_content_1=low1_first_level_save, low_performance_ability_show_more_content_2=low2_first_level_save, current_habits_of_ability_show_more_content_1=current1_first_level_save, current_habits_of_ability_show_more_content_2=current2_first_level_save, habitats_outside_of_me_show_more_content_1=habitats1_first_level_save, habitats_outside_of_me_show_more_content_2=habitats2_first_level_save)
                                if worksheet.cell_value(2,3)== "":
                                    Errors.append("Please provide current reality order to insert")
                        except:
                            Errors.append("Error in current reality "+worksheet.cell_value(2,1)+" code")
                        
                        if check==False:
                            Success.append(current_reality_save.name+ " current reality added successfully")
                except:
                    Errors.append("File is closed")
                
                try:
                    os.remove(delete_file)
                except:
                    Errors.append("not deleted")
            except: 
                Errors.append("File is not saved, nor opened") 
        return render(request, 'causalforces/uploadcsv.html', {
                "Errors":Errors,
                "Success":Success,
                "warning":warning,
            })
