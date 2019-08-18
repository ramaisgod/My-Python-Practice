from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from bgc.models import Location
from .forms import *
from .models import *
from django.db.models import Q
import datetime

final_bgc_id = 0


def bgc_form(request):
    context = {
    }
    return render(request, 'bgc_form2.html', context)


# Bellow function to split full name
def split_name(name):
    name = name.split()
    f_name = name[0]
    a = name[1:len(name) - 1]
    m_name = " ".join(a)
    l_name = name[-1]
    name_dict = {"first_name": f_name, "middle_name": m_name, "last_name": l_name}
    return name_dict


# Bellow Code to go Initiation form according to employee type
def search_candidate(request):
    context = {
        'form': SearchForm(),
        'emp_type': None,
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'crf_info': None,
        'CC_list': CriticalClient.objects.all(),
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_proceed' in request.POST):
        form = SearchForm(request.POST)
        global emp_type
        emp_type = request.POST.get('emp_type')
        context['emp_type'] = emp_type
        if (emp_type == 'Freelancer') or (emp_type == 'Intern') or (emp_type == 'Vendor Staff'):
            context['emp_type'] = emp_type
            return render(request, 'initiation_form.html', context)
        elif (emp_type == 'Full Time Employee') or (emp_type == 'Business Associate') or (emp_type == 'Retainers'):
            context['emp_type'] = emp_type
            context['form'] = form
            return render(request, 'search.html', context)
        else:
            context['emp_type'] = None
            return render(request, 'search.html', context)
    elif (request.method == 'POST') and ('btn_search' in request.POST):
        global searchID
        searchID = str(request.POST.get('searchID').strip())
        # search_count = NcpDtDump.objects.filter(reference_id=searchID).count()
        count_ncp_dt = NcpDtDump.objects.filter(reference_id=searchID.upper()).count()
        count_ncp_ct = NcpCtDump.objects.filter(reference_id=searchID.upper()).count()
        count_grs = Grsdump.objects.filter(ep_reference_id=searchID.upper()).count()
        try:
            count_dhc = DhcReport.objects.filter(employee_field=float(searchID)).count()
        except:
            count_dhc = 0
        if count_ncp_dt > 0:
            context['obj_data_ncp_dt'] = NcpDtDump.objects.filter(reference_id=searchID.upper()).first()
        elif count_ncp_ct > 0:
            context['obj_data_ncp_ct'] = NcpCtDump.objects.filter(reference_id=searchID.upper()).first()
        elif count_grs > 0:
            context['obj_data_grs_dump'] = Grsdump.objects.filter(ep_reference_id=searchID.upper()).first()
        else:
            try:
                context['obj_data_dhc_dump'] = DhcReport.objects.filter(employee_field=float(searchID)).first()
            except:
                pass
        context['emp_type'] = emp_type
        context['form'] = SearchForm(request.POST)
        context['emp_type'] = emp_type
        context['search_count'] = max(count_ncp_dt, count_ncp_ct, count_grs, count_dhc)
        return render(request, 'search.html', context)
    elif (request.method == 'POST') and ('btn_initiation' in request.POST) and (searchID[0:2].lower() == 'dt'):
        obj_data_ncp_dt = NcpDtDump.objects.filter(reference_id=searchID.upper()).first()
        context['obj_data_ncp_dt'] = obj_data_ncp_dt
        full_name = split_name(name=obj_data_ncp_dt.candidate_name)
        context['first_name'] = full_name['first_name']
        context['middle_name'] = full_name['middle_name']
        context['last_name'] = full_name['last_name']
        context['emp_type'] = emp_type
        return render(request, 'initiation_form.html', context)
    elif (request.method == 'POST') and ('btn_initiation' in request.POST) and (searchID[0:2].lower() == 'ct'):
        obj_data_ncp_ct = NcpCtDump.objects.filter(reference_id=searchID.upper()).first()
        context['obj_data_ncp_ct'] = obj_data_ncp_ct
        full_name = split_name(name=obj_data_ncp_ct.candidate_name)
        context['first_name'] = full_name['first_name']
        context['middle_name'] = full_name['middle_name']
        context['last_name'] = full_name['last_name']
        context['emp_type'] = emp_type
        return render(request, 'initiation_form.html', context)
    elif (request.method == 'POST') and ('btn_initiation' in request.POST) and (searchID[0:2].lower() == 'ep'):
        obj_data_grs_dump = Grsdump.objects.filter(ep_reference_id=searchID.upper()).first()
        context['obj_data_grs_dump'] = obj_data_grs_dump
        full_name = split_name(name=obj_data_grs_dump.candidate_name)
        context['first_name'] = full_name['first_name']
        context['middle_name'] = full_name['middle_name']
        context['last_name'] = full_name['last_name']
        context['emp_type'] = emp_type
        return render(request, 'initiation_form.html', context)

    return render(request, 'search.html', context)


# Bellow code to check application completetion
def is_initiation_form_completed(request, id):
    app = BGCInitiation.objects.get(id=id)
    if (request.user.is_superuser) or (request.user.is_staff):
        if app.Employee_Type is "Experienced":
            if (app.Is_Candidate_Info is True) and (app.Is_CRF_Info is True) and (app.Is_Billing_Info is True) and (
                    app.Is_Mandatory_Info is True) and (app.Is_Educational_Info is True) and (
                    app.Is_Employment_Info is True) and (app.Is_CSC_Check is True) and (app.Is_BGC_Check is True):
                return 1
            else:
                return 0
        else:
            if (app.Is_Candidate_Info is True) and (app.Is_CRF_Info is True) and (app.Is_Billing_Info is True) and (
                    app.Is_Mandatory_Info is True) and (app.Is_Educational_Info is True) and (
                    app.Is_CSC_Check is True) and (app.Is_BGC_Check is True):
                return 1
            else:
                return 0
    elif request.user.is_implant:
        if app.Employee_Type is "Experienced":
            if (app.Is_Candidate_Info is True) and (app.Is_CRF_Info is True) and (app.Is_Billing_Info is True) and (
                    app.Is_Mandatory_Info is True) and (app.Is_Educational_Info is True) and (
                    app.Is_Employment_Info is True) and (app.Is_CSC_Check is True):
                return 1
            else:
                return 0
        else:
            if (app.Is_Candidate_Info is True) and (app.Is_CRF_Info is True) and (app.Is_Billing_Info is True) and (
                    app.Is_Mandatory_Info is True) and (app.Is_Educational_Info is True) and (
                    app.Is_CSC_Check is True):
                return 1
            else:
                return 0
    else:
        return 0


# Bellow Code validate initiation form
def validate_form(request, edu_hire, edu, mode, approval, status):
    if edu_hire == edu:
        if mode == 'Full Time':
            return 1
        else:
            if (approval == 'Required') and (status == 'Approved'):
                return 1
            else:
                return 0
    else:
        return 1


# Bellow Code populate list of saved initiation form
def bgc_application_list(request):
    context = {}
    if request.user.is_implant:
        obj_app = BGCInitiation.objects.filter(Q(BGC_Status='SUBMITTED') | Q(BGC_Status='INITIATED'), Maker_ID=request.user.username).order_by('-Last_Modified')
        context['obj_app'] = obj_app
        return render(request, 'list_application.html', context)
    else:
        obj_app = BGCInitiation.objects.filter(Q(BGC_Status='SUBMITTED') | Q(BGC_Status='INITIATED')).order_by('-Last_Modified')
        context['obj_app'] = obj_app
        return render(request, 'list_application.html', context)


def bgc_mywork_list(request):
    context = {}
    if request.user.is_implant:
        obj_app = BGCInitiation.objects.filter(BGC_Status='SAVED AS DRAFT', Maker_ID=request.user.username).order_by('-Last_Modified')
        context['obj_app'] = obj_app
        return render(request, 'list_myworklist.html', context)
    else:
        obj_app = BGCInitiation.objects.filter(Q(BGC_Status='SUBMITTED') | Q(BGC_Status='INITIATED') | Q(BGC_Status='SAVED AS DRAFT'), Q(Maker_ID=request.user.username) | Q(Checker_ID=request.user.username)).order_by('-Last_Modified')
        context['obj_app'] = obj_app
        return render(request, 'list_myworklist.html', context)


# Bellow code to open saved initiation form
def initiation_form_view(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
        'obj_bgc': obj_bgc,
    }
    return render(request, 'view_initiation_form.html', context)


# Below code to edit saved application
def edit_candidate_info(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
        'obj_bgc': obj_bgc,
    }
    if (request.method == 'POST') and ('btn_candidate_update' in request.POST):
        # obj_bgc = BGCInitiation.objects.filter(id=id).first()
        # candidate_form.Reference_ID = request.POST.get('ep_dt_number').strip()
        # candidate_form.Applicant_ID = request.POST.get('applicant_id').strip()
        # candidate_form.Employee_ID = request.POST.get('employee_id').strip()
        obj_bgc.First_Name = request.POST.get('f_name').strip().title()
        obj_bgc.Middle_Name = request.POST.get('m_name').strip().title()
        obj_bgc.Last_Name = request.POST.get('l_name').strip().title()
        obj_bgc.Candidate_Full_Name = obj_bgc.First_Name + ' ' + obj_bgc.Middle_Name + ' ' + obj_bgc.Last_Name
        obj_bgc.Candidate_Full_Name_After_Marriage = request.POST.get('name_after_marriage').strip().title()
        # obj_bgc.Email = request.POST.get('email')
        obj_bgc.Alternate_Email = request.POST.get('alt_email').strip().lower()
        obj_bgc.Phone = request.POST.get('phone').strip()
        obj_bgc.Alternate_Phone = request.POST.get('alt_phone').strip()
        obj_bgc.Marital_Status = request.POST.get('marital_status')
        obj_bgc.Gender = request.POST.get('gender')
        try:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%m-%Y").date()
        except:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%b-%Y").date()
        obj_bgc.Date_of_Birth = dob  # datetime.datetime.strptime(request.POST.get('dob'), '%d-%m-%Y')
        obj_bgc.Father_Name = request.POST.get('father_name').strip().title()
        obj_bgc.Spouse_Name = request.POST.get('spouse_name').strip().title()
        obj_bgc.Candidate_Status = request.POST.get('candidate_status').strip().upper()
        try:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%m-%Y").date()
        except:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%b-%Y").date()
        obj_bgc.Joining_Date = doj  # datetime.datetime.strptime(request.POST.get('doj'), '%d-%m-%Y')
        obj_bgc.Joining_Status = request.POST.get('joining_status').strip().upper()
        obj_bgc.Location = request.POST.get('location')
        obj_bgc.Sub_Location = request.POST.get('sub_location')
        obj_bgc.Employee_Type = request.POST.get('employee_type')
        obj_bgc.Qualification_for_Hire = request.POST.get('qualification_to_hire')
        obj_bgc.Initiated_By = request.POST.get('initiated_by').strip()
        obj_bgc.Last_Modified = datetime.datetime.now()
        obj_bgc.save()
        context['message_candidate'] = 'Updated !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_crf_info(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST':
        crf = float(request.POST.get('crf_number').strip())
        rpm_dump = RpmDump.objects.filter(crf_backfill_code=crf).first()
        context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
        context['crf_info'] = request.POST
        if 'btn_crf_find' in request.POST:
            row_count = RpmDump.objects.filter(crf_backfill_code=crf).count()
            if (row_count <= 0) or (len(str(crf)) < 5):
                context['message_crf'] = 'CRF number not found !!!'
                context['crf_info'] = request.POST
                context['row_count'] = row_count
                return render(request, 'view_initiation_form.html', context)
            else:
                context['rpm_dump'] = rpm_dump
                context['crf_info'] = request.POST
                context['obj_bgc'] = BGCInitiation.objects.get(id=id)
                context['row_count'] = row_count
                context['message_crf'] = 'CRF Found !!!'
                return render(request, 'view_initiation_form.html', context)
        elif 'btn_crf_show_checks' in request.POST:
            cc_code = request.POST.get('customer_code')
            cc_checks = CriticalClient.objects.filter(CC_Code=cc_code).first()
            context['rpm_dump'] = rpm_dump
            context['crf_info'] = request.POST
            context['cc_checks'] = cc_checks
            context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
            context['obj_bgc'] = BGCInitiation.objects.get(id=id)
            # context['message_crf'] = 'CRF Found !!!'
            return render(request, 'view_initiation_form.html', context)
        elif 'btn_crf_save' in request.POST:
            if RpmDump.objects.filter(crf_backfill_code=crf).count() <= 0:
                context['row_count'] = 0
                context['crf_info'] = request.POST
                context['obj_bgc'] = BGCInitiation.objects.get(id=id)
                context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
                context['message_crf'] = 'CRF number not found !!!'
                return render(request, 'view_initiation_form.html', context)
            else:
                cc_code = request.POST.get('customer_code')
                cc = request.POST.get('critical_client')
                if (cc == 'Yes') and (cc_code == '--NA--'):
                    context['message_crf'] = 'Please select valid customer code'
                    context['rpm_dump'] = rpm_dump
                    context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
                    context['crf_info'] = request.POST
                    context['obj_bgc'] = BGCInitiation.objects.get(id=id)
                    return render(request, 'view_initiation_form.html', context)
                elif (cc == 'No') and (cc_code != '--NA--'):
                    context['message_crf'] = "Please select Customer Code '--NA--' in case of non critical customer"
                    context['rpm_dump'] = rpm_dump
                    context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
                    context['crf_info'] = request.POST
                    context['obj_bgc'] = BGCInitiation.objects.get(id=id)
                    return render(request, 'view_initiation_form.html', context)
                else:
                    crf_form = BGCInitiation.objects.get(id=id)
                    crf_form.CRF_Number = request.POST.get('crf_number')
                    crf_form.WON_SWON = request.POST.get('won_swon')
                    crf_form.Critical_Client = request.POST.get('critical_client')
                    Customer_Code = request.POST.get('customer_code').strip()
                    crf_form.Customer_Code = Customer_Code
                    crf_form.Customer_Name = request.POST.get('customer_name').strip()
                    if Customer_Code == "--NA--":
                        crf_form.CC_Database_Check = '--NA--'
                        crf_form.CC_Identity_Check = '--NA--'
                        crf_form.CC_Address_Check = '--NA--'
                        crf_form.CC_Criminal_Check = '--NA--'
                        crf_form.CC_Court_Check = '--NA--'
                        crf_form.CC_Passport_Check = '--NA--'
                        crf_form.CC_Education_Check = '--NA--'
                        crf_form.CC_Employment_Check = '--NA--'
                        crf_form.CC_Credit_Check = '--NA--'
                        crf_form.CC_Facis_Check = '--NA--'
                        crf_form.CC_Reference_Check = '--NA--'
                        crf_form.CC_Social_Media_Check = '--NA--'
                        crf_form.CC_Comments = '--NA--'
                        crf_form.Is_CRF_Info = True
                        crf_form.Last_Modified = datetime.datetime.now()
                    else:
                        cc_checks = CriticalClient.objects.filter(CC_Code=Customer_Code).first()
                        crf_form.CC_Database_Check = cc_checks.Database_Check
                        crf_form.CC_Identity_Check = cc_checks.Identity_Check
                        crf_form.CC_Address_Check = cc_checks.Address_Check
                        crf_form.CC_Criminal_Check = cc_checks.Criminal_Check
                        crf_form.CC_Court_Check = cc_checks.Court_Check
                        crf_form.CC_Passport_Check = cc_checks.Passport_Check
                        crf_form.CC_Education_Check = cc_checks.Education_Check
                        crf_form.CC_Employment_Check = cc_checks.Employment_Check
                        crf_form.CC_Credit_Check = cc_checks.Credit_Check
                        crf_form.CC_Facis_Check = cc_checks.Facis_Check
                        crf_form.CC_Reference_Check = cc_checks.Reference_Check
                        crf_form.CC_Social_Media_Check = cc_checks.Social_Media_Check
                        crf_form.CC_Comments = cc_checks.Comments
                        crf_form.Is_CRF_Info = True
                        crf_form.Last_Modified = datetime.datetime.now()
                    crf_form.save()
                    context['rpm_dump'] = rpm_dump
                    context['crf_info'] = request.POST
                    context['message_crf'] = 'Data has been Saved !!!'
                    obj_bgc = BGCInitiation.objects.get(id=id)
                    context['obj_bgc'] = obj_bgc
                    context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
                    return render(request, 'view_initiation_form.html', context)
        else:
            return render(request, 'view_initiation_form.html', context)


def edit_billing_info(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_billing' in request.POST):
        won_swon = request.POST.get('won_swon_billing').strip()
        row_count = DhcReport.objects.filter(project_field=won_swon).count()
        if row_count <= 0:
            context['row_count'] = row_count
            context['billing_info'] = request.POST
            context['message_billing'] = 'Invalid WON/SWON !!!'
            context['dhc_report_billing'] = DhcReport.objects.filter(project_field=won_swon)
            return render(request, 'view_initiation_form.html', context)
        else:
            billing_form = BGCInitiation.objects.get(id=id)
            billing_form.WON_SWON_for_Billing = request.POST.get('won_swon_billing')
            billing_form.Project_Number_Billing = 'NULL'
            billing_form.Project_Name_Billing = request.POST.get('project_name_billing').strip()
            billing_form.Project_Start_Date = datetime.datetime.strptime(request.POST.get('project_start_date'), '%d-%m-%Y')
            billing_form.Project_End_Date = datetime.datetime.strptime(request.POST.get('project_end_date'), '%d-%m-%Y')
            billing_form.Project_Status = request.POST.get('project_status')
            billing_form.Is_Billing_Info = True
            billing_form.Last_Modified = datetime.datetime.now()
            billing_form.save()
            billing_info = request.POST
            context['billing_info'] = billing_info
            context['message_billing'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            context['row_count'] = row_count
            return render(request, 'view_initiation_form.html', context)
    elif (request.method == 'POST') and ('btn_billing_find' in request.POST):
        won_swon = request.POST.get('won_swon_billing')
        row_count = DhcReport.objects.filter(project_field=won_swon).count()
        dhc_report_billing = DhcReport.objects.filter(project_field=won_swon).first()
        context['dhc_report_billing'] = dhc_report_billing
        context['row_count'] = row_count
        context['billing_info'] = request.POST
        if row_count <= 0:
            context['message_billing'] = 'Invalid WON/SWON !!!'
            context['row_count'] = row_count
            context['dhc_report_billing'] = dhc_report_billing
            return render(request, 'view_initiation_form.html', context)
        else:
            dhc_report_billing = DhcReport.objects.filter(project_field=won_swon).first()
            context['dhc_report_billing'] = dhc_report_billing
            context['billing_info'] = request.POST
            context['message_billing'] = 'WON/SWON Found !!!'
            context['row_count'] = row_count
            return render(request, 'view_initiation_form.html', context)
    else:
        return render(request, 'view_initiation_form.html', context)


def edit_mandatory_docs(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_mandatory' in request.POST):
        mandatory_form = BGCInitiation.objects.get(id=id)
        mandatory_form.Photo_ID_Proof = request.POST.get('photo_id_proof')
        mandatory_form.Address_Proof = request.POST.get('address_proof')
        mandatory_form.Medical_Certificate = request.POST.get('medical_cert')
        mandatory_form.Is_Mandatory_Info = True
        mandatory_form.Last_Modified = datetime.datetime.now()
        mandatory_form.save()
        context['message_mandatory'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        mandatory_info = request.POST
        context['mandatory_info'] = mandatory_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_edu_ssc(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_ssc' in request.POST:
        edu_form = BGCInitiation.objects.get(id=id)
        edu_form.SSC_Name_of_Examination_Passed = request.POST.get('ssc_exam_passed').strip()
        edu_form.SSC_Mode_of_Education = request.POST.get('ssc_mode_edu')
        edu_form.SSC_Approval = request.POST.get('ssc_approval')
        edu_form.SSC_Approval_Status = request.POST.get('ssc_approval_status')
        edu_form.SSC_All_Semester_Marksheet = 'Yes' if request.POST.get('ssc_marksheet') == 'on' else 'No'
        edu_form.SSC_Passing_Certificate = 'Yes' if request.POST.get('ssc_pass_cert') == 'on' else 'No'
        edu_form.SSC_Hall_Ticket = 'Yes' if request.POST.get('ssc_hall_ticket') == 'on' else 'No'
        edu_form.SSC_Online_Snapshot = 'Yes' if request.POST.get('ssc_online_ss') == 'on' else 'No'
        edu_form.SSC_ATKT = 'Yes' if request.POST.get('ssc_atkt') == 'on' else 'No'
        edu_form.SSC_Convocation = 'Yes' if request.POST.get('ssc_con_degree') == 'on' else 'No'
        edu_form.SSC_Declaration = 'Yes' if request.POST.get('ssc_decl') == 'on' else 'No'
        edu_form.SSC_Document_Status = request.POST.get('ssc_doc_status')
        edu_form.SSC_Expected_Days = 0 if request.POST.get('ssc_days') == '' else request.POST.get('ssc_days')
        edu_form.SSC_Remarks = request.POST.get('ssc_remarks')
        edu_form.Is_Educational_Info = True
        edu_form.Last_Modified = datetime.datetime.now()
        edu_form.save()
        context['message_edu_ssc'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        edu_ssc = request.POST
        context['edu_ssc'] = edu_ssc
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_edu_hsc(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_hsc' in request.POST:
        bgc = BGCInitiation.objects.get(id=id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('hsc_mode_edu')
        approval = request.POST.get('hsc_approval')
        status = request.POST.get('hsc_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='HSC', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_hsc'] = 'Wrong input please check !!!'
            context['edu_hsc'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=id)
            edu_form.HSC_Name_of_Examination_Passed = request.POST.get('hsc_exam_passed').strip()
            edu_form.HSC_Mode_of_Education = request.POST.get('hsc_mode_edu')
            edu_form.HSC_Approval = request.POST.get('hsc_approval')
            edu_form.HSC_Approval_Status = request.POST.get('hsc_approval_status')
            edu_form.HSC_All_Semester_Marksheet = 'Yes' if request.POST.get('hsc_marksheet') == 'on' else 'No'
            edu_form.HSC_Passing_Certificate = 'Yes' if request.POST.get('hsc_pass_cert') == 'on' else 'No'
            edu_form.HSC_Hall_Ticket = 'Yes' if request.POST.get('hsc_hall_ticket') == 'on' else 'No'
            edu_form.HSC_Online_Snapshot = 'Yes' if request.POST.get('hsc_online_ss') == 'on' else 'No'
            edu_form.HSC_ATKT = 'Yes' if request.POST.get('hsc_atkt') == 'on' else 'No'
            edu_form.HSC_Convocation = 'Yes' if request.POST.get('hsc_con_degree') == 'on' else 'No'
            edu_form.HSC_Declaration = 'Yes' if request.POST.get('hsc_decl') == 'on' else 'No'
            edu_form.HSC_Document_Status = request.POST.get('hsc_doc_status')
            edu_form.HSC_Expected_Days = 0 if request.POST.get('hsc_days') == '' else request.POST.get('hsc_days')
            edu_form.HSC_Remarks = request.POST.get('hsc_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_hsc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            edu_hsc = request.POST
            context['edu_hsc'] = edu_hsc
            return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_edu_graduation(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_graduation' in request.POST:
        bgc = BGCInitiation.objects.get(id=id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('graduation_mode_edu')
        approval = request.POST.get('graduation_approval')
        status = request.POST.get('graduation_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='Graduation', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_graduation'] = 'Wrong input please check !!!'
            context['edu_graduation'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=id)
            edu_form.Graduation_Name_of_Examination_Passed = request.POST.get('graduation_exam_passed').strip()
            edu_form.Graduation_Mode_of_Education = request.POST.get('graduation_mode_edu')
            edu_form.Graduation_Approval = request.POST.get('graduation_approval')
            edu_form.Graduation_Approval_Status = request.POST.get('graduation_approval_status')
            edu_form.Graduation_All_Semester_Marksheet = 'Yes' if request.POST.get('graduation_marksheet') == 'on' else 'No'
            edu_form.Graduation_Passing_Certificate = 'Yes' if request.POST.get('graduation_pass_cert') == 'on' else 'No'
            edu_form.Graduation_Hall_Ticket = 'Yes' if request.POST.get('graduation_hall_ticket') == 'on' else 'No'
            edu_form.Graduation_Online_Snapshot = 'Yes' if request.POST.get('graduation_online_ss') == 'on' else 'No'
            edu_form.Graduation_ATKT = 'Yes' if request.POST.get('graduation_atkt') == 'on' else 'No'
            edu_form.Graduation_Convocation = 'Yes' if request.POST.get('graduation_con_degree') == 'on' else 'No'
            edu_form.Graduation_Declaration = 'Yes' if request.POST.get('graduation_decl') == 'on' else 'No'
            edu_form.Graduation_Document_Status = request.POST.get('graduation_doc_status')
            edu_form.Graduation_Expected_Days = 0 if request.POST.get('graduation_days') == '' else request.POST.get('graduation_days')
            edu_form.Graduation_Remarks = request.POST.get('graduation_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_graduation'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            edu_graduation = request.POST
            context['edu_graduation'] = edu_graduation
            return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_edu_post_graduation(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_post_graduation' in request.POST:
        bgc = BGCInitiation.objects.get(id=id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('post_graduation_mode_edu')
        approval = request.POST.get('post_graduation_approval')
        status = request.POST.get('post_graduation_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='Post Graduation', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_post_graduation'] = 'Wrong input please check !!!'
            context['edu_post_graduation'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=id)
            edu_form.Post_Graduation_Name_of_Examination_Passed = request.POST.get('post_graduation_exam_passed').strip()
            edu_form.Post_Graduation_Mode_of_Education = request.POST.get('post_graduation_mode_edu')
            edu_form.Post_Graduation_Approval = request.POST.get('post_graduation_approval')
            edu_form.Post_Graduation_Approval_Status = request.POST.get('post_graduation_approval_status')
            edu_form.Post_Graduation_All_Semester_Marksheet = 'Yes' if request.POST.get('post_graduation_marksheet') == 'on' else 'No'
            edu_form.Post_Graduation_Passing_Certificate = 'Yes' if request.POST.get('post_graduation_pass_cert') == 'on' else 'No'
            edu_form.Post_Graduation_Hall_Ticket = 'Yes' if request.POST.get('post_graduation_hall_ticket') == 'on' else 'No'
            edu_form.Post_Graduation_Online_Snapshot = 'Yes' if request.POST.get('post_graduation_online_ss') == 'on' else 'No'
            edu_form.Post_Graduation_ATKT = 'Yes' if request.POST.get('post_graduation_atkt') == 'on' else 'No'
            edu_form.Post_Graduation_Convocation = 'Yes' if request.POST.get('post_graduation_con_degree') == 'on' else 'No'
            edu_form.Post_Graduation_Declaration = 'Yes' if request.POST.get('post_graduation_decl') == 'on' else 'No'
            edu_form.Post_Graduation_Document_Status = request.POST.get('post_graduation_doc_status')
            edu_form.Post_Graduation_Expected_Days = 0 if request.POST.get('post_graduation_days') == '' else request.POST.get('post_graduation_days')
            edu_form.Post_Graduation_Remarks = request.POST.get('post_graduation_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_post_graduation'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            edu_post_graduation = request.POST
            context['edu_post_graduation'] = edu_post_graduation
            return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_edu_diploma(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_diploma' in request.POST:
        edu_form = BGCInitiation.objects.get(id=id)
        edu_form.Diploma_Name_of_Examination_Passed = request.POST.get('diploma_exam_passed').strip()
        edu_form.Diploma_Mode_of_Education = request.POST.get('diploma_mode_edu')
        edu_form.Diploma_Approval = request.POST.get('diploma_approval')
        edu_form.Diploma_Approval_Status = request.POST.get('diploma_approval_status')
        edu_form.Diploma_All_Semester_Marksheet = 'Yes' if request.POST.get('diploma_marksheet') == 'on' else 'No'
        edu_form.Diploma_Passing_Certificate = 'Yes' if request.POST.get('diploma_pass_cert') == 'on' else 'No'
        edu_form.Diploma_Hall_Ticket = 'Yes' if request.POST.get('diploma_hall_ticket') == 'on' else 'No'
        edu_form.Diploma_Online_Snapshot = 'Yes' if request.POST.get('diploma_online_ss') == 'on' else 'No'
        edu_form.Diploma_ATKT = 'Yes' if request.POST.get('diploma_atkt') == 'on' else 'No'
        edu_form.Diploma_Convocation = 'Yes' if request.POST.get('diploma_con_degree') == 'on' else 'No'
        edu_form.Diploma_Declaration = 'Yes' if request.POST.get('diploma_decl') == 'on' else 'No'
        edu_form.Diploma_Document_Status = request.POST.get('diploma_doc_status')
        edu_form.Diploma_Expected_Days = 0 if request.POST.get('diploma_days') == '' else request.POST.get('diploma_days')
        edu_form.Diploma_Remarks = request.POST.get('diploma_remarks')
        edu_form.Is_Educational_Info = True
        edu_form.Last_Modified = datetime.datetime.now()
        edu_form.save()
        context['message_edu_diploma'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        edu_diploma = request.POST
        context['edu_diploma'] = edu_diploma
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_current(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_current' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.Current_Company_Name = request.POST.get('current_company_name').strip()
        emp_form.Current_Status = request.POST.get('current_company_status')
        emp_form.Current_Deviation = request.POST.get('current_company_dev')
        emp_form.Current_Offer_Letter = 'Yes' if request.POST.get('current_ol') == 'on' else 'No'
        emp_form.Current_Salary_Slip = 'Yes' if request.POST.get('current_ss') == 'on' else 'No'
        emp_form.Current_Salary_Certificate = 'Yes' if request.POST.get('current_sc') == 'on' else 'No'
        emp_form.Current_Bank_Statement = 'Yes' if request.POST.get('current_bs') == 'on' else 'No'
        emp_form.Current_Experience_Letter = 'Yes' if request.POST.get('current_el') == 'on' else 'No'
        emp_form.Current_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('current_ral') == 'on' else 'No'
        emp_form.Current_Relieving_Letter = 'Yes' if request.POST.get('current_rel') == 'on' else 'No'
        emp_form.Current_Service_Certificate = 'Yes' if request.POST.get('current_ser_cert') == 'on' else 'No'
        emp_form.Current_Declaration = 'Yes' if request.POST.get('current_decl') == 'on' else 'No'
        emp_form.Current_Document_Status = request.POST.get('current_doc_status')
        emp_form.Current_Expected_Days = 0 if request.POST.get('current_days') == '' else request.POST.get('current_days')
        emp_form.Current_Remarks = request.POST.get('current_remarks').strip()
        emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_current'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp1(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp1' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E1_Company_Name = request.POST.get('emp1_company_name').strip()
        emp_form.E1_Status = request.POST.get('emp1_company_status')
        emp_form.E1_Deviation = request.POST.get('emp1_company_dev')
        emp_form.E1_Offer_Letter = 'Yes' if request.POST.get('emp1_ol') == 'on' else 'No'
        emp_form.E1_Salary_Slip = 'Yes' if request.POST.get('emp1_ss') == 'on' else 'No'
        emp_form.E1_Salary_Certificate = 'Yes' if request.POST.get('emp1_sc') == 'on' else 'No'
        emp_form.E1_Bank_Statement = 'Yes' if request.POST.get('emp1_bs') == 'on' else 'No'
        emp_form.E1_Experience_Letter = 'Yes' if request.POST.get('emp1_el') == 'on' else 'No'
        emp_form.E1_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp1_ral') == 'on' else 'No'
        emp_form.E1_Relieving_Letter = 'Yes' if request.POST.get('emp1_rel') == 'on' else 'No'
        emp_form.E1_Service_Certificate = 'Yes' if request.POST.get('emp1_ser_cert') == 'on' else 'No'
        emp_form.E1_Declaration = 'Yes' if request.POST.get('emp1_decl') == 'on' else 'No'
        emp_form.E1_Document_Status = request.POST.get('emp1_doc_status')
        emp_form.E1_Expected_Days = 0 if request.POST.get('emp1_days') == '' else request.POST.get('emp1_days')
        emp_form.E1_Remarks = request.POST.get('emp1_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp1'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp2(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp2' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E2_Company_Name = request.POST.get('emp2_company_name').strip()
        emp_form.E2_Status = request.POST.get('emp2_company_status')
        emp_form.E2_Deviation = request.POST.get('emp2_company_dev')
        emp_form.E2_Offer_Letter = 'Yes' if request.POST.get('emp2_ol') == 'on' else 'No'
        emp_form.E2_Salary_Slip = 'Yes' if request.POST.get('emp2_ss') == 'on' else 'No'
        emp_form.E2_Salary_Certificate = 'Yes' if request.POST.get('emp2_sc') == 'on' else 'No'
        emp_form.E2_Bank_Statement = 'Yes' if request.POST.get('emp2_bs') == 'on' else 'No'
        emp_form.E2_Experience_Letter = 'Yes' if request.POST.get('emp2_el') == 'on' else 'No'
        emp_form.E2_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp2_ral') == 'on' else 'No'
        emp_form.E2_Relieving_Letter = 'Yes' if request.POST.get('emp2_rel') == 'on' else 'No'
        emp_form.E2_Service_Certificate = 'Yes' if request.POST.get('emp2_ser_cert') == 'on' else 'No'
        emp_form.E2_Declaration = 'Yes' if request.POST.get('emp2_decl') == 'on' else 'No'
        emp_form.E2_Document_Status = request.POST.get('emp2_doc_status')
        emp_form.E2_Expected_Days = 0 if request.POST.get('emp2_days') == '' else request.POST.get('emp2_days')
        emp_form.E2_Remarks = request.POST.get('emp2_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp2'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp3(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp3' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E3_Company_Name = request.POST.get('emp3_company_name').strip()
        emp_form.E3_Status = request.POST.get('emp3_company_status')
        emp_form.E3_Deviation = request.POST.get('emp3_company_dev')
        emp_form.E3_Offer_Letter = 'Yes' if request.POST.get('emp3_ol') == 'on' else 'No'
        emp_form.E3_Salary_Slip = 'Yes' if request.POST.get('emp3_ss') == 'on' else 'No'
        emp_form.E3_Salary_Certificate = 'Yes' if request.POST.get('emp3_sc') == 'on' else 'No'
        emp_form.E3_Bank_Statement = 'Yes' if request.POST.get('emp3_bs') == 'on' else 'No'
        emp_form.E3_Experience_Letter = 'Yes' if request.POST.get('emp3_el') == 'on' else 'No'
        emp_form.E3_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp3_ral') == 'on' else 'No'
        emp_form.E3_Relieving_Letter = 'Yes' if request.POST.get('emp3_rel') == 'on' else 'No'
        emp_form.E3_Service_Certificate = 'Yes' if request.POST.get('emp3_ser_cert') == 'on' else 'No'
        emp_form.E3_Declaration = 'Yes' if request.POST.get('emp3_decl') == 'on' else 'No'
        emp_form.E3_Document_Status = request.POST.get('emp3_doc_status')
        emp_form.E3_Expected_Days = 0 if request.POST.get('emp3_days') == '' else request.POST.get('emp3_days')
        emp_form.E3_Remarks = request.POST.get('emp3_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp3'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp4(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp4' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E4_Company_Name = request.POST.get('emp4_company_name').strip()
        emp_form.E4_Status = request.POST.get('emp4_company_status')
        emp_form.E4_Deviation = request.POST.get('emp4_company_dev')
        emp_form.E4_Offer_Letter = 'Yes' if request.POST.get('emp4_ol') == 'on' else 'No'
        emp_form.E4_Salary_Slip = 'Yes' if request.POST.get('emp4_ss') == 'on' else 'No'
        emp_form.E4_Salary_Certificate = 'Yes' if request.POST.get('emp4_sc') == 'on' else 'No'
        emp_form.E4_Bank_Statement = 'Yes' if request.POST.get('emp4_bs') == 'on' else 'No'
        emp_form.E4_Experience_Letter = 'Yes' if request.POST.get('emp4_el') == 'on' else 'No'
        emp_form.E4_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp4_ral') == 'on' else 'No'
        emp_form.E4_Relieving_Letter = 'Yes' if request.POST.get('emp4_rel') == 'on' else 'No'
        emp_form.E4_Service_Certificate = 'Yes' if request.POST.get('emp4_ser_cert') == 'on' else 'No'
        emp_form.E4_Declaration = 'Yes' if request.POST.get('emp4_decl') == 'on' else 'No'
        emp_form.E4_Document_Status = request.POST.get('emp4_doc_status')
        emp_form.E4_Expected_Days = 0 if request.POST.get('emp4_days') == '' else request.POST.get('emp4_days')
        emp_form.E4_Remarks = request.POST.get('emp4_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp4'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp5(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp5' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E5_Company_Name = request.POST.get('emp5_company_name').strip()
        emp_form.E5_Status = request.POST.get('emp5_company_status')
        emp_form.E5_Deviation = request.POST.get('emp5_company_dev')
        emp_form.E5_Offer_Letter = 'Yes' if request.POST.get('emp5_ol') == 'on' else 'No'
        emp_form.E5_Salary_Slip = 'Yes' if request.POST.get('emp5_ss') == 'on' else 'No'
        emp_form.E5_Salary_Certificate = 'Yes' if request.POST.get('emp5_sc') == 'on' else 'No'
        emp_form.E5_Bank_Statement = 'Yes' if request.POST.get('emp5_bs') == 'on' else 'No'
        emp_form.E5_Experience_Letter = 'Yes' if request.POST.get('emp5_el') == 'on' else 'No'
        emp_form.E5_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp5_ral') == 'on' else 'No'
        emp_form.E5_Relieving_Letter = 'Yes' if request.POST.get('emp5_rel') == 'on' else 'No'
        emp_form.E5_Service_Certificate = 'Yes' if request.POST.get('emp5_ser_cert') == 'on' else 'No'
        emp_form.E5_Declaration = 'Yes' if request.POST.get('emp5_decl') == 'on' else 'No'
        emp_form.E5_Document_Status = request.POST.get('emp5_doc_status')
        emp_form.E5_Expected_Days = 0 if request.POST.get('emp5_days') == '' else request.POST.get('emp5_days')
        emp_form.E5_Remarks = request.POST.get('emp5_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp5'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp6(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp6' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E6_Company_Name = request.POST.get('emp6_company_name').strip()
        emp_form.E6_Status = request.POST.get('emp6_company_status')
        emp_form.E6_Deviation = request.POST.get('emp6_company_dev')
        emp_form.E6_Offer_Letter = 'Yes' if request.POST.get('emp6_ol') == 'on' else 'No'
        emp_form.E6_Salary_Slip = 'Yes' if request.POST.get('emp6_ss') == 'on' else 'No'
        emp_form.E6_Salary_Certificate = 'Yes' if request.POST.get('emp6_sc') == 'on' else 'No'
        emp_form.E6_Bank_Statement = 'Yes' if request.POST.get('emp6_bs') == 'on' else 'No'
        emp_form.E6_Experience_Letter = 'Yes' if request.POST.get('emp6_el') == 'on' else 'No'
        emp_form.E6_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp6_ral') == 'on' else 'No'
        emp_form.E6_Relieving_Letter = 'Yes' if request.POST.get('emp6_rel') == 'on' else 'No'
        emp_form.E6_Service_Certificate = 'Yes' if request.POST.get('emp6_ser_cert') == 'on' else 'No'
        emp_form.E6_Declaration = 'Yes' if request.POST.get('emp6_decl') == 'on' else 'No'
        emp_form.E6_Document_Status = request.POST.get('emp6_doc_status')
        emp_form.E6_Expected_Days = 0 if request.POST.get('emp6_days') == '' else request.POST.get('emp6_days')
        emp_form.E6_Remarks = request.POST.get('emp6_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp6'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_emp_emp7(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp7' in request.POST:
        emp_form = BGCInitiation.objects.get(id=id)
        emp_form.E7_Company_Name = request.POST.get('emp7_company_name').strip()
        emp_form.E7_Status = request.POST.get('emp7_company_status')
        emp_form.E7_Deviation = request.POST.get('emp7_company_dev')
        emp_form.E7_Offer_Letter = 'Yes' if request.POST.get('emp7_ol') == 'on' else 'No'
        emp_form.E7_Salary_Slip = 'Yes' if request.POST.get('emp7_ss') == 'on' else 'No'
        emp_form.E7_Salary_Certificate = 'Yes' if request.POST.get('emp7_sc') == 'on' else 'No'
        emp_form.E7_Bank_Statement = 'Yes' if request.POST.get('emp7_bs') == 'on' else 'No'
        emp_form.E7_Experience_Letter = 'Yes' if request.POST.get('emp7_el') == 'on' else 'No'
        emp_form.E7_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp7_ral') == 'on' else 'No'
        emp_form.E7_Relieving_Letter = 'Yes' if request.POST.get('emp7_rel') == 'on' else 'No'
        emp_form.E7_Service_Certificate = 'Yes' if request.POST.get('emp7_ser_cert') == 'on' else 'No'
        emp_form.E7_Declaration = 'Yes' if request.POST.get('emp7_decl') == 'on' else 'No'
        emp_form.E7_Document_Status = request.POST.get('emp7_doc_status')
        emp_form.E7_Expected_Days = 0 if request.POST.get('emp7_days') == '' else request.POST.get('emp7_days')
        emp_form.E7_Remarks = request.POST.get('emp7_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp7'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def edit_csc(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_csc' in request.POST:
        bgc_obj = BGCInitiation.objects.get(id=id)
        doc_check = bgc_obj.Is_Mandatory_Info
        if (request.POST.get('drug_test') == 'on') and ((request.POST.get('drug_test_panel') == '') or (request.POST.get('drug_test_panel') == '0')):
            context['csc_info'] = request.POST
            context['message_csc'] = 'Please select drug test panel number !!!'
            return render(request, 'view_initiation_form.html', context)
        elif ((request.POST.get('court_check') == 'on') or (request.POST.get('cibil_check') == 'on')) and (doc_check is False):
            context['csc_info'] = request.POST
            context['message_csc'] = 'Please complete mandatory documents first!!!'
            return render(request, 'view_initiation_form.html', context)
        else:
            csc_form = BGCInitiation.objects.get(id=id)
            csc_form.Drug_Test = 'Yes' if request.POST.get('drug_test') == 'on' else 'No'
            csc_form.Court_Check = 'Yes' if request.POST.get('court_check') == 'on' else 'No'
            csc_form.Cibil_Check = 'Yes' if request.POST.get('cibil_check') == 'on' else 'No'
            csc_form.Social_Media_Check = 'Yes' if request.POST.get('social_media_check') == 'on' else 'No'
            csc_form.UK_Treasury_Check = 'Yes' if request.POST.get('uk_treasury_check') == 'on' else 'No'
            csc_form.Freddie_Mac_Check = 'Yes' if request.POST.get('freddie_mac_check') == 'on' else 'No'
            csc_form.Facis_Check = 'Yes' if request.POST.get('facis_check') == 'on' else 'No'
            csc_form.Drug_Test_Panel = 0 if request.POST.get('drug_test_panel') == '' else request.POST.get('drug_test_panel')
            csc_form.Remarks_for_Client_Specific_Check = request.POST.get('csc_remarks').strip()
            csc_form.Is_CSC_Check = True
            csc_form.Last_Modified = datetime.datetime.now()
            csc_form.save()
            context['message_csc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            csc_info = request.POST
            context['csc_info'] = csc_info
            return render(request, 'view_initiation_form.html', context)
    else:
        return render(request, 'view_initiation_form.html', context)


def edit_bgc_check(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_bgc_check' in request.POST:
        bgc_obj = BGCInitiation.objects.get(id=id)
        doc_check_mandatory = bgc_obj.Is_Mandatory_Info
        doc_check_edu = bgc_obj.Is_Educational_Info
        doc_check_emp = bgc_obj.Is_Employment_Info
        check_crf = bgc_obj.Is_CRF_Info
        check_billing = bgc_obj.Is_Billing_Info
        if ((request.POST.get('present_address') == 'on') or (request.POST.get('permanent_address') == 'on') or (request.POST.get('present_address_criminal') == 'on') or (request.POST.get('permanent_address_criminal') == 'on') or (request.POST.get('identity') == 'on')) and (doc_check_mandatory is False):
            context['message_bgc'] = 'Please complete mandatory documents !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        elif bgc_obj.Is_Candidate_Info is False:
            context['message_bgc'] = 'Candidate details are missing  !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        elif (request.POST.get('highest_edu') == 'on') and (doc_check_edu is False):
            context['message_bgc'] = 'Please complete educational details !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        elif (request.POST.get('employment') == 'on') and (doc_check_emp is False):
            context['message_bgc'] = 'Please complete employment details !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        elif (check_crf is False) and (check_billing is False):
            context['message_bgc'] = 'CRF / WON-SWON for billing are missing  !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'view_initiation_form.html', context)
        else:
            bgc_check_form = BGCInitiation.objects.get(id=id)
            bgc_check_form.Present_Address_Check = 'Yes' if request.POST.get('present_address') == 'on' else 'No'
            bgc_check_form.Present_Address_Criminal_Check = 'Yes' if request.POST.get(
                'present_address_criminal') == 'on' else 'No'
            bgc_check_form.Permanent_Address_Check = 'Yes' if request.POST.get('permanent_address') == 'on' else 'No'
            bgc_check_form.Permanent_Address_Criminal_Check = 'Yes' if request.POST.get(
                'permanent_address_criminal') == 'on' else 'No'
            bgc_check_form.Highest_Education_Check = 'Yes' if request.POST.get('highest_edu') == 'on' else 'No'
            bgc_check_form.Employment_Check = 'Yes' if request.POST.get('employment') == 'on' else 'No'
            bgc_check_form.Identity_Check = 'Yes' if request.POST.get('identity') == 'on' else 'No'
            bgc_check_form.Database_Check = 'Yes' if request.POST.get('database') == 'on' else 'No'
            bgc_check_form.Reference_Check = 'Yes' if request.POST.get('reference') == 'on' else 'No'
            bgc_check_form.Is_BGC_Check = True
            bgc_check_form.Last_Modified = datetime.datetime.now()
            bgc_check_form.BGC_Status = 'SUBMITTED'
            bgc_check_form.save()
            context['message_bgc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=id)
            context['obj_bgc'] = obj_bgc
            bgc_check_info = request.POST
            context['bgc_check_info'] = bgc_check_info
            return render(request, 'view_initiation_form.html', context)
    else:
        context['bgc_check_info'] = request.POST
        return render(request, 'view_initiation_form.html', context)


def edit_vendor(request, id=None):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_vendor' in request.POST:
        vendor_form = BGCInitiation.objects.get(id=id)
        vendor_form.Vendor_Name = request.POST.get('vendor_name')
        try:
            Initiation_Date = datetime.datetime.strptime(request.POST.get('initiation_date'), '%d-%m-%Y')
        except:
            Initiation_Date = datetime.datetime.strptime(request.POST.get('initiation_date'), '%d-%b-%Y')
        vendor_form.Initiation_Date = Initiation_Date
        vendor_form.Checker_Name = request.user.first_name
        vendor_form.Checker_ID = request.user.username
        vendor_form.Remarks = request.POST.get('vendor_remarks').strip()
        vendor_form.Is_Vendor = True
        vendor_form.Last_Modified = datetime.datetime.now()
        vendor_form.BGC_Status = 'INITIATED'
        # Generate Unique Code
        BGC_Unique_Code = generate_unique_code(id=id, is_drug_test=obj_bgc.Drug_Test,
                                               is_critical_client=obj_bgc.Critical_Client)
        vendor_form.BGC_Unique_Code = BGC_Unique_Code.upper()
        vendor_form.save()
        context['vendor_form_fields'] = VendorFormFields(request.POST)
        context['message_vendor'] = 'Successfully Initiated. BGC Code is ' + BGC_Unique_Code.upper()
        obj_bgc = BGCInitiation.objects.get(id=id)
        context['obj_bgc'] = obj_bgc
        vendor_info = request.POST
        context['vendor_info'] = vendor_info
        return render(request, 'view_initiation_form.html', context)
    return render(request, 'view_initiation_form.html', context)


def generate_unique_code(id, is_drug_test, is_critical_client):
    if (is_drug_test == 'Yes') and (is_critical_client == 'Yes'):
        obj_bgc = BGCInitiation.objects.get(id=id)
        row_count = BGCInitiation.objects.all().count() + 1
        location = obj_bgc.Location[0]
        sub_location = obj_bgc.Sub_Location[0:2]
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return location + sub_location + current_datetime + str(row_count) + 'C' + 'D'
    elif (is_drug_test == 'Yes') and (is_critical_client == 'No' or is_critical_client == None):
        obj_bgc = BGCInitiation.objects.get(id=id)
        row_count = BGCInitiation.objects.all().count() + 1
        location = obj_bgc.Location[0]
        sub_location = obj_bgc.Sub_Location[0:2]
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return location + sub_location + current_datetime + str(row_count) + 'D'
    elif (is_drug_test == 'No' or is_drug_test == None) and (is_critical_client == 'Yes'):
        obj_bgc = BGCInitiation.objects.get(id=id)
        row_count = BGCInitiation.objects.all().count() + 1
        location = obj_bgc.Location[0]
        sub_location = obj_bgc.Sub_Location[0:2]
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return location + sub_location + current_datetime + str(row_count) + 'C'
    else:
        obj_bgc = BGCInitiation.objects.get(id=id)
        row_count = BGCInitiation.objects.all().count() + 1
        location = obj_bgc.Location[0]
        sub_location = obj_bgc.Sub_Location[0:2]
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return location + sub_location + current_datetime + str(row_count)


# Save initiation form
def save_candidate_info(request):
    from .models import Location
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': None,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_candidate_save' in request.POST):
        # CANDIDATE INFORMATION
        BGC_For = emp_type
        Reference_ID = 'NA' if (emp_type == 'Freelancer') or (emp_type == 'Intern') or (emp_type == 'Vendor Staff') else request.POST.get('ep_dt_number')
        Applicant_ID = 'NA' if (emp_type == 'Freelancer') or (emp_type == 'Intern') or (emp_type == 'Vendor Staff') else request.POST.get('applicant_id')
        Employee_ID = 'NA' if (emp_type == 'Freelancer') or (emp_type == 'Intern') or (emp_type == 'Vendor Staff') else request.POST.get('employee_id')
        First_Name = request.POST.get('f_name').strip()
        Middle_Name = request.POST.get('m_name').strip()
        Last_Name = request.POST.get('l_name').strip()
        Candidate_Full_Name = First_Name + ' ' + Middle_Name + ' ' + Last_Name
        Candidate_Full_Name_After_Marriage = request.POST.get('name_after_marriage').strip()
        Email = request.POST.get('email').strip()
        Alternate_Email = request.POST.get('alt_email').strip()
        Phone = request.POST.get('phone').strip()
        Alternate_Phone = request.POST.get('alt_phone').strip()
        Marital_Status = request.POST.get('marital_status')
        Gender = request.POST.get('gender')
        try:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%m-%Y").date()
        except:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%b-%Y").date()
        Date_of_Birth = dob  # datetime.datetime.strptime(request.POST.get('dob'), '%d-%m-%Y')
        Father_Name = request.POST.get('father_name').strip()
        Spouse_Name = request.POST.get('spouse_name').strip()
        Candidate_Status = 'NA' if request.POST.get('candidate_status') == '' else request.POST.get('candidate_status').strip()
        try:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%m-%Y").date()
        except:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%b-%Y").date()
        Joining_Date = doj  # datetime.datetime.strptime(request.POST.get('doj'), '%d-%m-%Y')
        Joining_Status = 'NA' if request.POST.get('joining_status') == '' else request.POST.get('joining_status').strip()
        Location = request.POST.get('location')
        Sub_Location = request.POST.get('sub_location')
        Employee_Type = request.POST.get('employee_type')
        Qualification_for_Hire = request.POST.get('qualification_to_hire')
        Initiated_By = request.POST.get('initiated_by').strip()
        # BGC_Unique_Code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(row_count)
        bgc_obj = BGCInitiation(BGC_For=BGC_For,
                                Reference_ID=Reference_ID, Applicant_ID=Applicant_ID, Employee_ID=Employee_ID,
                                First_Name=First_Name.title(), Middle_Name=Middle_Name.title(),
                                Last_Name=Last_Name.title(),
                                Candidate_Full_Name=Candidate_Full_Name.title(),
                                Candidate_Full_Name_After_Marriage=Candidate_Full_Name_After_Marriage.title(),
                                Email=Email.lower(),
                                Alternate_Email=Alternate_Email.lower(), Phone=Phone,
                                Alternate_Phone=Alternate_Phone,
                                Marital_Status=Marital_Status, Gender=Gender, Date_of_Birth=Date_of_Birth,
                                Father_Name=Father_Name.title(), Spouse_Name=Spouse_Name.title(),
                                Candidate_Status=Candidate_Status.upper(),
                                Joining_Date=Joining_Date, Joining_Status=Joining_Status.upper(), Location=Location,
                                Sub_Location=Sub_Location, Employee_Type=Employee_Type,
                                Qualification_for_Hire=Qualification_for_Hire, Initiated_By=Initiated_By)
        bgc_obj.save()
        BGCInitiation.objects.filter(id=bgc_obj.pk).update(Is_Candidate_Info=True)
        BGCInitiation.objects.filter(id=bgc_obj.pk).update(Maker_ID=request.user.username)
        BGCInitiation.objects.filter(id=bgc_obj.pk).update(BGC_Status='SAVED AS DRAFT')
        BGCInitiation.objects.filter(id=bgc_obj.pk).update(Last_Modified=datetime.datetime.now())
        global final_bgc_id
        final_bgc_id = bgc_obj.pk
        context['bgc_id'] = final_bgc_id
        context['message_candidate'] = 'Data has been Saved !!!'
        candidate_info = request.POST
        context['candidate_info'] = candidate_info
        return render(request, 'initiation_form.html', context)
    elif (request.method == 'POST') and ('btn_candidate_update' in request.POST):
        # final_bgc_id = request.POST.get('bgc_id')
        candidate_form = BGCInitiation.objects.get(id=final_bgc_id)
        # candidate_form.Reference_ID = request.POST.get('ep_dt_number').strip()
        # candidate_form.Applicant_ID = request.POST.get('applicant_id').strip()
        # candidate_form.Employee_ID = request.POST.get('employee_id').strip()
        candidate_form.First_Name = request.POST.get('f_name').strip().title()
        candidate_form.Middle_Name = request.POST.get('m_name').strip().title()
        candidate_form.Last_Name = request.POST.get('l_name').strip().title()
        candidate_form.Candidate_Full_Name = candidate_form.First_Name + ' ' + candidate_form.Middle_Name + ' ' + candidate_form.Last_Name
        candidate_form.Candidate_Full_Name_After_Marriage = request.POST.get('name_after_marriage').strip().title()
        # candidate_form.Email = request.POST.get('email')
        candidate_form.Alternate_Email = request.POST.get('alt_email').strip().lower()
        candidate_form.Phone = request.POST.get('phone').strip()
        candidate_form.Alternate_Phone = request.POST.get('alt_phone').strip()
        candidate_form.Marital_Status = request.POST.get('marital_status')
        candidate_form.Gender = request.POST.get('gender')
        try:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%m-%Y").date()
        except:
            dob = datetime.datetime.strptime(request.POST.get('dob'), "%d-%b-%Y").date()
        candidate_form.Date_of_Birth = dob  # datetime.datetime.strptime(request.POST.get('dob'), '%d-%m-%Y')
        candidate_form.Father_Name = request.POST.get('father_name').strip().title()
        candidate_form.Spouse_Name = request.POST.get('spouse_name').strip().title()
        candidate_form.Candidate_Status = request.POST.get('candidate_status').strip().upper()
        try:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%m-%Y").date()
        except:
            doj = datetime.datetime.strptime(request.POST.get('doj'), "%d-%b-%Y").date()
        candidate_form.Joining_Date = doj  # datetime.datetime.strptime(request.POST.get('doj'), '%d-%m-%Y')
        candidate_form.Joining_Status = request.POST.get('joining_status').strip().upper()
        candidate_form.Location = request.POST.get('location')
        candidate_form.Sub_Location = request.POST.get('sub_location')
        candidate_form.Employee_Type = request.POST.get('employee_type')
        candidate_form.Qualification_for_Hire = request.POST.get('qualification_to_hire')
        candidate_form.Initiated_By = request.POST.get('initiated_by').strip()
        candidate_form.Last_Modified = datetime.datetime.now()
        candidate_form.save()
        candidate_info = request.POST
        context['candidate_info'] = candidate_info
        context['message_candidate'] = 'Updated !!!'
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_crf_info(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST':
        crf = request.POST.get('crf_number')
        rpm_dump = RpmDump.objects.filter(crf_backfill_code=crf).first()
        context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
        context['crf_info'] = request.POST
        if 'btn_crf_find' in request.POST:
            row_count = RpmDump.objects.filter(crf_backfill_code=crf).count()
            if row_count <= 0:
                context['message_crf'] = 'CRF number not found !!!'
                context['crf_info'] = request.POST
                context['row_count'] = row_count
                return render(request, 'initiation_form.html', context)
            else:
                context['rpm_dump'] = rpm_dump
                context['crf_info'] = request.POST
                context['row_count'] = row_count
                context['message_crf'] = 'CRF Found !!!'
                return render(request, 'initiation_form.html', context)
        elif 'btn_crf_show_checks' in request.POST:
            cc_code = request.POST.get('customer_code')
            cc_checks = CriticalClient.objects.filter(CC_Code=cc_code).first()
            context['rpm_dump'] = rpm_dump
            context['crf_info'] = request.POST
            context['cc_checks'] = cc_checks
            context['row_count'] = RpmDump.objects.filter(crf_backfill_code=crf).count()
            return render(request, 'initiation_form.html', context)
        elif 'btn_crf_save' in request.POST:
            crf = request.POST.get('crf_number')
            row_count = RpmDump.objects.filter(crf_backfill_code=crf).count()
            if row_count <= 0:
                context['row_count'] = row_count
                context['crf_info'] = request.POST
                context['message_crf'] = 'CRF number not found !!!'
                return render(request, 'initiation_form.html', context)
            else:
                cc_code = request.POST.get('customer_code')
                cc = request.POST.get('critical_client')
                if (cc == 'Yes') and (cc_code == '--NA--'):
                    context['message_crf'] = 'Please select valid customer code'
                    context['rpm_dump'] = rpm_dump
                    context['row_count'] = row_count
                    context['crf_info'] = request.POST
                    # context['obj_bgc'] = BGCInitiation.objects.get(id=final_bgc_id)
                    # context['dhc_report'] = dhc_report
                    return render(request, 'initiation_form.html', context)
                elif (cc == 'No') and (cc_code != '--NA--'):
                    context['message_crf'] = "Please select Customer Code '--NA--' in case of non critical customer"
                    context['rpm_dump'] = rpm_dump
                    context['row_count'] = row_count
                    context['crf_info'] = request.POST
                    # context['obj_bgc'] = BGCInitiation.objects.get(id=final_bgc_id)
                    # context['dhc_report'] = dhc_report
                    return render(request, 'initiation_form.html', context)
                else:
                    crf_form = BGCInitiation.objects.get(id=final_bgc_id)
                    crf_form.CRF_Number = request.POST.get('crf_number')
                    crf_form.WON_SWON = request.POST.get('won_swon')
                    crf_form.Critical_Client = request.POST.get('critical_client')
                    Customer_Code = request.POST.get('customer_code').strip()
                    crf_form.Customer_Code = Customer_Code
                    crf_form.Customer_Name = request.POST.get('customer_name').strip()
                    if Customer_Code == "--NA--":
                        crf_form.CC_Database_Check = '--NA--'
                        crf_form.CC_Identity_Check = '--NA--'
                        crf_form.CC_Address_Check = '--NA--'
                        crf_form.CC_Criminal_Check = '--NA--'
                        crf_form.CC_Court_Check = '--NA--'
                        crf_form.CC_Passport_Check = '--NA--'
                        crf_form.CC_Education_Check = '--NA--'
                        crf_form.CC_Employment_Check = '--NA--'
                        crf_form.CC_Credit_Check = '--NA--'
                        crf_form.CC_Facis_Check = '--NA--'
                        crf_form.CC_Reference_Check = '--NA--'
                        crf_form.CC_Social_Media_Check = '--NA--'
                        crf_form.CC_Comments = '--NA--'
                        crf_form.Is_CRF_Info = True
                        crf_form.Last_Modified = datetime.datetime.now()
                    else:
                        cc_checks = CriticalClient.objects.filter(CC_Code=Customer_Code).first()
                        crf_form.CC_Database_Check = cc_checks.Database_Check
                        crf_form.CC_Identity_Check = cc_checks.Identity_Check
                        crf_form.CC_Address_Check = cc_checks.Address_Check
                        crf_form.CC_Criminal_Check = cc_checks.Criminal_Check
                        crf_form.CC_Court_Check = cc_checks.Court_Check
                        crf_form.CC_Passport_Check = cc_checks.Passport_Check
                        crf_form.CC_Education_Check = cc_checks.Education_Check
                        crf_form.CC_Employment_Check = cc_checks.Employment_Check
                        crf_form.CC_Credit_Check = cc_checks.Credit_Check
                        crf_form.CC_Facis_Check = cc_checks.Facis_Check
                        crf_form.CC_Reference_Check = cc_checks.Reference_Check
                        crf_form.CC_Social_Media_Check = cc_checks.Social_Media_Check
                        crf_form.CC_Comments = cc_checks.Comments
                        crf_form.Is_CRF_Info = True
                        crf_form.Last_Modified = datetime.datetime.now()
                    crf_form.save()
                    context['rpm_dump'] = rpm_dump
                    context['crf_info'] = request.POST
                    context['message_crf'] = 'Data has been Saved !!!'
                    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
                    context['obj_bgc'] = obj_bgc
                    context['row_count'] = 0
                    return render(request, 'initiation_form.html', context)
        else:
            return render(request, 'initiation_form.html', context)


def save_billing_info(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_billing' in request.POST):
        won_swon = request.POST.get('won_swon_billing').strip()
        row_count = DhcReport.objects.filter(project_field=won_swon).count()
        if row_count <= 0:
            context['row_count'] = row_count
            context['billing_info'] = request.POST
            context['message_billing'] = 'Invalid WON/SWON !!!'
            context['dhc_report_billing'] = DhcReport.objects.filter(project_field=won_swon)
            return render(request, 'initiation_form.html', context)
        else:
            billing_form = BGCInitiation.objects.get(id=final_bgc_id)
            billing_form.WON_SWON_for_Billing = request.POST.get('won_swon_billing')
            billing_form.Project_Number_Billing = 'NULL'
            billing_form.Project_Name_Billing = request.POST.get('project_name_billing').strip()
            billing_form.Project_Start_Date = datetime.datetime.strptime(request.POST.get('project_start_date'), '%d-%m-%Y')
            billing_form.Project_End_Date = datetime.datetime.strptime(request.POST.get('project_end_date'), '%d-%m-%Y')
            billing_form.Project_Status = request.POST.get('project_status')
            billing_form.Is_Billing_Info = True
            billing_form.Last_Modified = datetime.datetime.now()
            billing_form.save()
            billing_info = request.POST
            context['billing_info'] = billing_info
            context['message_billing'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            context['row_count'] = 0
            return render(request, 'initiation_form.html', context)
    elif (request.method == 'POST') and ('btn_billing_find' in request.POST):
        won_swon = request.POST.get('won_swon_billing')
        row_count = DhcReport.objects.filter(project_field=won_swon).count()
        dhc_report_billing = DhcReport.objects.filter(project_field=won_swon).first()
        context['dhc_report_billing'] = dhc_report_billing
        context['row_count'] = row_count
        context['billing_info'] = request.POST
        if row_count <= 0:
            context['message_billing'] = 'Invalid WON/SWON !!!'
            context['row_count'] = row_count
            context['dhc_report_billing'] = dhc_report_billing
            return render(request, 'initiation_form.html', context)
        else:
            dhc_report_billing = DhcReport.objects.filter(project_field=won_swon).first()
            context['dhc_report_billing'] = dhc_report_billing
            context['billing_info'] = request.POST
            context['message_billing'] = 'WON/SWON Found !!!'
            context['row_count'] = row_count
            return render(request, 'initiation_form.html', context)
    else:
        return render(request, 'initiation_form.html', context)


def save_mandatory_docs(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if (request.method == 'POST') and ('btn_mandatory' in request.POST):
        mandatory_form = BGCInitiation.objects.get(id=final_bgc_id)
        mandatory_form.Photo_ID_Proof = request.POST.get('photo_id_proof')
        mandatory_form.Address_Proof = request.POST.get('address_proof')
        mandatory_form.Medical_Certificate = request.POST.get('medical_cert')
        mandatory_form.Is_Mandatory_Info = True
        mandatory_form.Last_Modified = datetime.datetime.now()
        mandatory_form.save()
        context['message_mandatory'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        mandatory_info = request.POST
        context['mandatory_info'] = mandatory_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_edu_ssc(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_ssc' in request.POST:
        edu_form = BGCInitiation.objects.get(id=final_bgc_id)
        edu_form.SSC_Name_of_Examination_Passed = request.POST.get('ssc_exam_passed').strip()
        edu_form.SSC_Mode_of_Education = request.POST.get('ssc_mode_edu')
        edu_form.SSC_Approval = request.POST.get('ssc_approval')
        edu_form.SSC_Approval_Status = request.POST.get('ssc_approval_status')
        edu_form.SSC_All_Semester_Marksheet = 'Yes' if request.POST.get('ssc_marksheet') == 'on' else 'No'
        edu_form.SSC_Passing_Certificate = 'Yes' if request.POST.get('ssc_pass_cert') == 'on' else 'No'
        edu_form.SSC_Hall_Ticket = 'Yes' if request.POST.get('ssc_hall_ticket') == 'on' else 'No'
        edu_form.SSC_Online_Snapshot = 'Yes' if request.POST.get('ssc_online_ss') == 'on' else 'No'
        edu_form.SSC_ATKT = 'Yes' if request.POST.get('ssc_atkt') == 'on' else 'No'
        edu_form.SSC_Convocation = 'Yes' if request.POST.get('ssc_con_degree') == 'on' else 'No'
        edu_form.SSC_Declaration = 'Yes' if request.POST.get('ssc_decl') == 'on' else 'No'
        edu_form.SSC_Document_Status = request.POST.get('ssc_doc_status')
        edu_form.SSC_Expected_Days = 0 if request.POST.get('ssc_days') == '' else request.POST.get('ssc_days')
        edu_form.SSC_Remarks = request.POST.get('ssc_remarks')
        edu_form.Is_Educational_Info = True
        edu_form.Last_Modified = datetime.datetime.now()
        edu_form.save()
        context['message_edu_ssc'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        edu_ssc = request.POST
        context['edu_ssc'] = edu_ssc
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_edu_hsc(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_hsc' in request.POST:
        bgc = BGCInitiation.objects.get(id=final_bgc_id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('hsc_mode_edu')
        approval = request.POST.get('hsc_approval')
        status = request.POST.get('hsc_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='HSC', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_hsc'] = 'Wrong input please check !!!'
            context['edu_hsc'] = request.POST
            return render(request, 'initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=final_bgc_id)
            edu_form.HSC_Name_of_Examination_Passed = request.POST.get('hsc_exam_passed').strip()
            edu_form.HSC_Mode_of_Education = request.POST.get('hsc_mode_edu')
            edu_form.HSC_Approval = request.POST.get('hsc_approval')
            edu_form.HSC_Approval_Status = request.POST.get('hsc_approval_status')
            edu_form.HSC_All_Semester_Marksheet = 'Yes' if request.POST.get('hsc_marksheet') == 'on' else 'No'
            edu_form.HSC_Passing_Certificate = 'Yes' if request.POST.get('hsc_pass_cert') == 'on' else 'No'
            edu_form.HSC_Hall_Ticket = 'Yes' if request.POST.get('hsc_hall_ticket') == 'on' else 'No'
            edu_form.HSC_Online_Snapshot = 'Yes' if request.POST.get('hsc_online_ss') == 'on' else 'No'
            edu_form.HSC_ATKT = 'Yes' if request.POST.get('hsc_atkt') == 'on' else 'No'
            edu_form.HSC_Convocation = 'Yes' if request.POST.get('hsc_con_degree') == 'on' else 'No'
            edu_form.HSC_Declaration = 'Yes' if request.POST.get('hsc_decl') == 'on' else 'No'
            edu_form.HSC_Document_Status = request.POST.get('hsc_doc_status')
            edu_form.HSC_Expected_Days = 0 if request.POST.get('hsc_days') == '' else request.POST.get('hsc_days')
            edu_form.HSC_Remarks = request.POST.get('hsc_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_hsc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            edu_hsc = request.POST
            context['edu_hsc'] = edu_hsc
            return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_edu_graduation(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_graduation' in request.POST:
        bgc = BGCInitiation.objects.get(id=final_bgc_id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('graduation_mode_edu')
        approval = request.POST.get('graduation_approval')
        status = request.POST.get('graduation_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='Graduation', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_graduation'] = 'Wrong input please check !!!'
            context['edu_graduation'] = request.POST
            return render(request, 'initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=final_bgc_id)
            edu_form.Graduation_Name_of_Examination_Passed = request.POST.get('graduation_exam_passed').strip()
            edu_form.Graduation_Mode_of_Education = request.POST.get('graduation_mode_edu')
            edu_form.Graduation_Approval = request.POST.get('graduation_approval')
            edu_form.Graduation_Approval_Status = request.POST.get('graduation_approval_status')
            edu_form.Graduation_All_Semester_Marksheet = 'Yes' if request.POST.get('graduation_marksheet') == 'on' else 'No'
            edu_form.Graduation_Passing_Certificate = 'Yes' if request.POST.get('graduation_pass_cert') == 'on' else 'No'
            edu_form.Graduation_Hall_Ticket = 'Yes' if request.POST.get('graduation_hall_ticket') == 'on' else 'No'
            edu_form.Graduation_Online_Snapshot = 'Yes' if request.POST.get('graduation_online_ss') == 'on' else 'No'
            edu_form.Graduation_ATKT = 'Yes' if request.POST.get('graduation_atkt') == 'on' else 'No'
            edu_form.Graduation_Convocation = 'Yes' if request.POST.get('graduation_con_degree') == 'on' else 'No'
            edu_form.Graduation_Declaration = 'Yes' if request.POST.get('graduation_decl') == 'on' else 'No'
            edu_form.Graduation_Document_Status = request.POST.get('graduation_doc_status')
            edu_form.Graduation_Expected_Days = 0 if request.POST.get('graduation_days') == '' else request.POST.get('graduation_days')
            edu_form.Graduation_Remarks = request.POST.get('graduation_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_graduation'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            edu_graduation = request.POST
            context['edu_graduation'] = edu_graduation
            return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_edu_post_graduation(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_post_graduation' in request.POST:
        bgc = BGCInitiation.objects.get(id=final_bgc_id)
        edu_hire = bgc.Qualification_for_Hire
        mode = request.POST.get('post_graduation_mode_edu')
        approval = request.POST.get('post_graduation_approval')
        status = request.POST.get('post_graduation_approval_status')
        if validate_form(request, edu_hire=edu_hire, edu='Post Graduation', mode=mode, approval=approval, status=status) == 0:
            context['message_edu_post_graduation'] = 'Wrong input please check !!!'
            context['edu_post_graduation'] = request.POST
            return render(request, 'initiation_form.html', context)
        else:
            edu_form = BGCInitiation.objects.get(id=final_bgc_id)
            edu_form.Post_Graduation_Name_of_Examination_Passed = request.POST.get('post_graduation_exam_passed').strip()
            edu_form.Post_Graduation_Mode_of_Education = request.POST.get('post_graduation_mode_edu')
            edu_form.Post_Graduation_Approval = request.POST.get('post_graduation_approval')
            edu_form.Post_Graduation_Approval_Status = request.POST.get('post_graduation_approval_status')
            edu_form.Post_Graduation_All_Semester_Marksheet = 'Yes' if request.POST.get('post_graduation_marksheet') == 'on' else 'No'
            edu_form.Post_Graduation_Passing_Certificate = 'Yes' if request.POST.get('post_graduation_pass_cert') == 'on' else 'No'
            edu_form.Post_Graduation_Hall_Ticket = 'Yes' if request.POST.get('post_graduation_hall_ticket') == 'on' else 'No'
            edu_form.Post_Graduation_Online_Snapshot = 'Yes' if request.POST.get('post_graduation_online_ss') == 'on' else 'No'
            edu_form.Post_Graduation_ATKT = 'Yes' if request.POST.get('post_graduation_atkt') == 'on' else 'No'
            edu_form.Post_Graduation_Convocation = 'Yes' if request.POST.get('post_graduation_con_degree') == 'on' else 'No'
            edu_form.Post_Graduation_Declaration = 'Yes' if request.POST.get('post_graduation_decl') == 'on' else 'No'
            edu_form.Post_Graduation_Document_Status = request.POST.get('post_graduation_doc_status')
            edu_form.Post_Graduation_Expected_Days = 0 if request.POST.get('post_graduation_days') == '' else request.POST.get('post_graduation_days')
            edu_form.Post_Graduation_Remarks = request.POST.get('post_graduation_remarks')
            edu_form.Is_Educational_Info = True
            edu_form.Last_Modified = datetime.datetime.now()
            edu_form.save()
            context['message_edu_post_graduation'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            edu_post_graduation = request.POST
            context['edu_post_graduation'] = edu_post_graduation
            return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_edu_diploma(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_edu_diploma' in request.POST:
        edu_form = BGCInitiation.objects.get(id=final_bgc_id)
        edu_form.Diploma_Name_of_Examination_Passed = request.POST.get('diploma_exam_passed').strip()
        edu_form.Diploma_Mode_of_Education = request.POST.get('diploma_mode_edu')
        edu_form.Diploma_Approval = request.POST.get('diploma_approval')
        edu_form.Diploma_Approval_Status = request.POST.get('diploma_approval_status')
        edu_form.Diploma_All_Semester_Marksheet = 'Yes' if request.POST.get('diploma_marksheet') == 'on' else 'No'
        edu_form.Diploma_Passing_Certificate = 'Yes' if request.POST.get('diploma_pass_cert') == 'on' else 'No'
        edu_form.Diploma_Hall_Ticket = 'Yes' if request.POST.get('diploma_hall_ticket') == 'on' else 'No'
        edu_form.Diploma_Online_Snapshot = 'Yes' if request.POST.get('diploma_online_ss') == 'on' else 'No'
        edu_form.Diploma_ATKT = 'Yes' if request.POST.get('diploma_atkt') == 'on' else 'No'
        edu_form.Diploma_Convocation = 'Yes' if request.POST.get('diploma_con_degree') == 'on' else 'No'
        edu_form.Diploma_Declaration = 'Yes' if request.POST.get('diploma_decl') == 'on' else 'No'
        edu_form.Diploma_Document_Status = request.POST.get('diploma_doc_status')
        edu_form.Diploma_Expected_Days = 0 if request.POST.get('diploma_days') == '' else request.POST.get('diploma_days')
        edu_form.Diploma_Remarks = request.POST.get('diploma_remarks')
        edu_form.Is_Educational_Info = True
        edu_form.Last_Modified = datetime.datetime.now()
        edu_form.save()
        context['message_edu_diploma'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        edu_diploma = request.POST
        context['edu_diploma'] = edu_diploma
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_current(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_current' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.Current_Company_Name = request.POST.get('current_company_name').strip()
        emp_form.Current_Status = request.POST.get('current_company_status')
        emp_form.Current_Deviation = request.POST.get('current_company_dev')
        emp_form.Current_Offer_Letter = 'Yes' if request.POST.get('current_ol') == 'on' else 'No'
        emp_form.Current_Salary_Slip = 'Yes' if request.POST.get('current_ss') == 'on' else 'No'
        emp_form.Current_Salary_Certificate = 'Yes' if request.POST.get('current_sc') == 'on' else 'No'
        emp_form.Current_Bank_Statement = 'Yes' if request.POST.get('current_bs') == 'on' else 'No'
        emp_form.Current_Experience_Letter = 'Yes' if request.POST.get('current_el') == 'on' else 'No'
        emp_form.Current_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('current_ral') == 'on' else 'No'
        emp_form.Current_Relieving_Letter = 'Yes' if request.POST.get('current_rel') == 'on' else 'No'
        emp_form.Current_Service_Certificate = 'Yes' if request.POST.get('current_ser_cert') == 'on' else 'No'
        emp_form.Current_Declaration = 'Yes' if request.POST.get('current_decl') == 'on' else 'No'
        emp_form.Current_Document_Status = request.POST.get('current_doc_status')
        emp_form.Current_Expected_Days = 0 if request.POST.get('current_days') == '' else request.POST.get('current_days')
        emp_form.Current_Remarks = request.POST.get('current_remarks').strip()
        emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_current'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp1(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp1' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E1_Company_Name = request.POST.get('emp1_company_name').strip()
        emp_form.E1_Status = request.POST.get('emp1_company_status')
        emp_form.E1_Deviation = request.POST.get('emp1_company_dev')
        emp_form.E1_Offer_Letter = 'Yes' if request.POST.get('emp1_ol') == 'on' else 'No'
        emp_form.E1_Salary_Slip = 'Yes' if request.POST.get('emp1_ss') == 'on' else 'No'
        emp_form.E1_Salary_Certificate = 'Yes' if request.POST.get('emp1_sc') == 'on' else 'No'
        emp_form.E1_Bank_Statement = 'Yes' if request.POST.get('emp1_bs') == 'on' else 'No'
        emp_form.E1_Experience_Letter = 'Yes' if request.POST.get('emp1_el') == 'on' else 'No'
        emp_form.E1_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp1_ral') == 'on' else 'No'
        emp_form.E1_Relieving_Letter = 'Yes' if request.POST.get('emp1_rel') == 'on' else 'No'
        emp_form.E1_Service_Certificate = 'Yes' if request.POST.get('emp1_ser_cert') == 'on' else 'No'
        emp_form.E1_Declaration = 'Yes' if request.POST.get('emp1_decl') == 'on' else 'No'
        emp_form.E1_Document_Status = request.POST.get('emp1_doc_status')
        emp_form.E1_Expected_Days = 0 if request.POST.get('emp1_days') == '' else request.POST.get('emp1_days')
        emp_form.E1_Remarks = request.POST.get('emp1_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp1'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp2(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp2' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E2_Company_Name = request.POST.get('emp2_company_name').strip()
        emp_form.E2_Status = request.POST.get('emp2_company_status')
        emp_form.E2_Deviation = request.POST.get('emp2_company_dev')
        emp_form.E2_Offer_Letter = 'Yes' if request.POST.get('emp2_ol') == 'on' else 'No'
        emp_form.E2_Salary_Slip = 'Yes' if request.POST.get('emp2_ss') == 'on' else 'No'
        emp_form.E2_Salary_Certificate = 'Yes' if request.POST.get('emp2_sc') == 'on' else 'No'
        emp_form.E2_Bank_Statement = 'Yes' if request.POST.get('emp2_bs') == 'on' else 'No'
        emp_form.E2_Experience_Letter = 'Yes' if request.POST.get('emp2_el') == 'on' else 'No'
        emp_form.E2_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp2_ral') == 'on' else 'No'
        emp_form.E2_Relieving_Letter = 'Yes' if request.POST.get('emp2_rel') == 'on' else 'No'
        emp_form.E2_Service_Certificate = 'Yes' if request.POST.get('emp2_ser_cert') == 'on' else 'No'
        emp_form.E2_Declaration = 'Yes' if request.POST.get('emp2_decl') == 'on' else 'No'
        emp_form.E2_Document_Status = request.POST.get('emp2_doc_status')
        emp_form.E2_Expected_Days = 0 if request.POST.get('emp2_days') == '' else request.POST.get('emp2_days')
        emp_form.E2_Remarks = request.POST.get('emp2_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp2'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp3(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp3' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E3_Company_Name = request.POST.get('emp3_company_name').strip()
        emp_form.E3_Status = request.POST.get('emp3_company_status')
        emp_form.E3_Deviation = request.POST.get('emp3_company_dev')
        emp_form.E3_Offer_Letter = 'Yes' if request.POST.get('emp3_ol') == 'on' else 'No'
        emp_form.E3_Salary_Slip = 'Yes' if request.POST.get('emp3_ss') == 'on' else 'No'
        emp_form.E3_Salary_Certificate = 'Yes' if request.POST.get('emp3_sc') == 'on' else 'No'
        emp_form.E3_Bank_Statement = 'Yes' if request.POST.get('emp3_bs') == 'on' else 'No'
        emp_form.E3_Experience_Letter = 'Yes' if request.POST.get('emp3_el') == 'on' else 'No'
        emp_form.E3_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp3_ral') == 'on' else 'No'
        emp_form.E3_Relieving_Letter = 'Yes' if request.POST.get('emp3_rel') == 'on' else 'No'
        emp_form.E3_Service_Certificate = 'Yes' if request.POST.get('emp3_ser_cert') == 'on' else 'No'
        emp_form.E3_Declaration = 'Yes' if request.POST.get('emp3_decl') == 'on' else 'No'
        emp_form.E3_Document_Status = request.POST.get('emp3_doc_status')
        emp_form.E3_Expected_Days = 0 if request.POST.get('emp3_days') == '' else request.POST.get('emp3_days')
        emp_form.E3_Remarks = request.POST.get('emp3_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp3'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp4(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp4' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E4_Company_Name = request.POST.get('emp4_company_name').strip()
        emp_form.E4_Status = request.POST.get('emp4_company_status')
        emp_form.E4_Deviation = request.POST.get('emp4_company_dev')
        emp_form.E4_Offer_Letter = 'Yes' if request.POST.get('emp4_ol') == 'on' else 'No'
        emp_form.E4_Salary_Slip = 'Yes' if request.POST.get('emp4_ss') == 'on' else 'No'
        emp_form.E4_Salary_Certificate = 'Yes' if request.POST.get('emp4_sc') == 'on' else 'No'
        emp_form.E4_Bank_Statement = 'Yes' if request.POST.get('emp4_bs') == 'on' else 'No'
        emp_form.E4_Experience_Letter = 'Yes' if request.POST.get('emp4_el') == 'on' else 'No'
        emp_form.E4_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp4_ral') == 'on' else 'No'
        emp_form.E4_Relieving_Letter = 'Yes' if request.POST.get('emp4_rel') == 'on' else 'No'
        emp_form.E4_Service_Certificate = 'Yes' if request.POST.get('emp4_ser_cert') == 'on' else 'No'
        emp_form.E4_Declaration = 'Yes' if request.POST.get('emp4_decl') == 'on' else 'No'
        emp_form.E4_Document_Status = request.POST.get('emp4_doc_status')
        emp_form.E4_Expected_Days = 0 if request.POST.get('emp4_days') == '' else request.POST.get('emp4_days')
        emp_form.E4_Remarks = request.POST.get('emp4_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp4'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp5(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp5' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E5_Company_Name = request.POST.get('emp5_company_name').strip()
        emp_form.E5_Status = request.POST.get('emp5_company_status')
        emp_form.E5_Deviation = request.POST.get('emp5_company_dev')
        emp_form.E5_Offer_Letter = 'Yes' if request.POST.get('emp5_ol') == 'on' else 'No'
        emp_form.E5_Salary_Slip = 'Yes' if request.POST.get('emp5_ss') == 'on' else 'No'
        emp_form.E5_Salary_Certificate = 'Yes' if request.POST.get('emp5_sc') == 'on' else 'No'
        emp_form.E5_Bank_Statement = 'Yes' if request.POST.get('emp5_bs') == 'on' else 'No'
        emp_form.E5_Experience_Letter = 'Yes' if request.POST.get('emp5_el') == 'on' else 'No'
        emp_form.E5_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp5_ral') == 'on' else 'No'
        emp_form.E5_Relieving_Letter = 'Yes' if request.POST.get('emp5_rel') == 'on' else 'No'
        emp_form.E5_Service_Certificate = 'Yes' if request.POST.get('emp5_ser_cert') == 'on' else 'No'
        emp_form.E5_Declaration = 'Yes' if request.POST.get('emp5_decl') == 'on' else 'No'
        emp_form.E5_Document_Status = request.POST.get('emp5_doc_status')
        emp_form.E5_Expected_Days = 0 if request.POST.get('emp5_days') == '' else request.POST.get('emp5_days')
        emp_form.E5_Remarks = request.POST.get('emp5_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp5'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp6(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp6' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E6_Company_Name = request.POST.get('emp6_company_name').strip()
        emp_form.E6_Status = request.POST.get('emp6_company_status')
        emp_form.E6_Deviation = request.POST.get('emp6_company_dev')
        emp_form.E6_Offer_Letter = 'Yes' if request.POST.get('emp6_ol') == 'on' else 'No'
        emp_form.E6_Salary_Slip = 'Yes' if request.POST.get('emp6_ss') == 'on' else 'No'
        emp_form.E6_Salary_Certificate = 'Yes' if request.POST.get('emp6_sc') == 'on' else 'No'
        emp_form.E6_Bank_Statement = 'Yes' if request.POST.get('emp6_bs') == 'on' else 'No'
        emp_form.E6_Experience_Letter = 'Yes' if request.POST.get('emp6_el') == 'on' else 'No'
        emp_form.E6_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp6_ral') == 'on' else 'No'
        emp_form.E6_Relieving_Letter = 'Yes' if request.POST.get('emp6_rel') == 'on' else 'No'
        emp_form.E6_Service_Certificate = 'Yes' if request.POST.get('emp6_ser_cert') == 'on' else 'No'
        emp_form.E6_Declaration = 'Yes' if request.POST.get('emp6_decl') == 'on' else 'No'
        emp_form.E6_Document_Status = request.POST.get('emp6_doc_status')
        emp_form.E6_Expected_Days = 0 if request.POST.get('emp6_days') == '' else request.POST.get('emp6_days')
        emp_form.E6_Remarks = request.POST.get('emp6_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp6'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_emp_emp7(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_emp_emp7' in request.POST:
        emp_form = BGCInitiation.objects.get(id=final_bgc_id)
        emp_form.E7_Company_Name = request.POST.get('emp7_company_name').strip()
        emp_form.E7_Status = request.POST.get('emp7_company_status')
        emp_form.E7_Deviation = request.POST.get('emp7_company_dev')
        emp_form.E7_Offer_Letter = 'Yes' if request.POST.get('emp7_ol') == 'on' else 'No'
        emp_form.E7_Salary_Slip = 'Yes' if request.POST.get('emp7_ss') == 'on' else 'No'
        emp_form.E7_Salary_Certificate = 'Yes' if request.POST.get('emp7_sc') == 'on' else 'No'
        emp_form.E7_Bank_Statement = 'Yes' if request.POST.get('emp7_bs') == 'on' else 'No'
        emp_form.E7_Experience_Letter = 'Yes' if request.POST.get('emp7_el') == 'on' else 'No'
        emp_form.E7_Resignation_Acceptance_Letter = 'Yes' if request.POST.get('emp7_ral') == 'on' else 'No'
        emp_form.E7_Relieving_Letter = 'Yes' if request.POST.get('emp7_rel') == 'on' else 'No'
        emp_form.E7_Service_Certificate = 'Yes' if request.POST.get('emp7_ser_cert') == 'on' else 'No'
        emp_form.E7_Declaration = 'Yes' if request.POST.get('emp7_decl') == 'on' else 'No'
        emp_form.E7_Document_Status = request.POST.get('emp7_doc_status')
        emp_form.E7_Expected_Days = 0 if request.POST.get('emp7_days') == '' else request.POST.get('emp7_days')
        emp_form.E7_Remarks = request.POST.get('emp7_remarks').strip()
        # emp_form.Is_Employment_Info = True
        emp_form.Last_Modified = datetime.datetime.now()
        emp_form.save()
        context['message_emp_emp7'] = 'Data has been Saved !!!'
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        emp_info = request.POST
        context['emp_info'] = emp_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)


def save_csc(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_csc' in request.POST:
        bgc_obj = BGCInitiation.objects.get(id=final_bgc_id)
        doc_check = bgc_obj.Is_Mandatory_Info
        if (request.POST.get('drug_test') == 'on') and ((request.POST.get('drug_test_panel') == '') or (request.POST.get('drug_test_panel') == '0')):
            context['csc_info'] = request.POST
            context['message_csc'] = 'Please select drug test panel number !!!'
            return render(request, 'initiation_form.html', context)
        elif ((request.POST.get('court_check') == 'on') or (request.POST.get('cibil_check') == 'on')) and (doc_check is False):
            context['csc_info'] = request.POST
            context['message_csc'] = 'Please complete mandatory documents first!!!'
            return render(request, 'initiation_form.html', context)
        else:
            csc_form = BGCInitiation.objects.get(id=final_bgc_id)
            csc_form.Drug_Test = 'Yes' if request.POST.get('drug_test') == 'on' else 'No'
            csc_form.Court_Check = 'Yes' if request.POST.get('court_check') == 'on' else 'No'
            csc_form.Cibil_Check = 'Yes' if request.POST.get('cibil_check') == 'on' else 'No'
            csc_form.Social_Media_Check = 'Yes' if request.POST.get('social_media_check') == 'on' else 'No'
            csc_form.UK_Treasury_Check = 'Yes' if request.POST.get('uk_treasury_check') == 'on' else 'No'
            csc_form.Freddie_Mac_Check = 'Yes' if request.POST.get('freddie_mac_check') == 'on' else 'No'
            csc_form.Facis_Check = 'Yes' if request.POST.get('facis_check') == 'on' else 'No'
            csc_form.Drug_Test_Panel = 0 if request.POST.get('drug_test_panel') == '' else request.POST.get('drug_test_panel')
            csc_form.Remarks_for_Client_Specific_Check = request.POST.get('csc_remarks').strip()
            csc_form.Is_CSC_Check = True
            csc_form.Last_Modified = datetime.datetime.now()
            csc_form.save()
            context['message_csc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            csc_info = request.POST
            context['csc_info'] = csc_info
            return render(request, 'initiation_form.html', context)
    else:
        return render(request, 'initiation_form.html', context)


def save_bgc_check(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_bgc_check' in request.POST:
        bgc_obj = BGCInitiation.objects.get(id=final_bgc_id)
        doc_check_mandatory = bgc_obj.Is_Mandatory_Info
        doc_check_edu = bgc_obj.Is_Educational_Info
        doc_check_emp = bgc_obj.Is_Employment_Info
        check_crf = bgc_obj.Is_CRF_Info
        check_billing = bgc_obj.Is_Billing_Info
        if ((request.POST.get('present_address') == 'on') or (request.POST.get('permanent_address') == 'on') or (request.POST.get('present_address_criminal') == 'on') or (request.POST.get('permanent_address_criminal') == 'on') or (request.POST.get('identity') == 'on')) and (doc_check_mandatory is False):
            context['message_bgc'] = 'Please complete mandatory documents !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'initiation_form.html', context)
        elif bgc_obj.Is_Candidate_Info is False:
            context['message_bgc'] = 'Candidate details are missing  !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'initiation_form.html', context)
        elif (request.POST.get('highest_edu') == 'on') and (doc_check_edu is False):
            context['message_bgc'] = 'Please complete educational details !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'initiation_form.html', context)
        elif (request.POST.get('employment') == 'on') and (doc_check_emp is False):
            context['message_bgc'] = 'Please complete employment details !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'initiation_form.html', context)
        elif (check_crf is False) and (check_billing is False):
            context['message_bgc'] = 'CRF / WON-SWON for billing are missing  !!!'
            context['bgc_check_info'] = request.POST
            return render(request, 'initiation_form.html', context)
        else:
            bgc_check_form = BGCInitiation.objects.get(id=final_bgc_id)
            bgc_check_form.Present_Address_Check = 'Yes' if request.POST.get('present_address') == 'on' else 'No'
            bgc_check_form.Present_Address_Criminal_Check = 'Yes' if request.POST.get(
                'present_address_criminal') == 'on' else 'No'
            bgc_check_form.Permanent_Address_Check = 'Yes' if request.POST.get('permanent_address') == 'on' else 'No'
            bgc_check_form.Permanent_Address_Criminal_Check = 'Yes' if request.POST.get(
                'permanent_address_criminal') == 'on' else 'No'
            bgc_check_form.Highest_Education_Check = 'Yes' if request.POST.get('highest_edu') == 'on' else 'No'
            bgc_check_form.Employment_Check = 'Yes' if request.POST.get('employment') == 'on' else 'No'
            bgc_check_form.Identity_Check = 'Yes' if request.POST.get('identity') == 'on' else 'No'
            bgc_check_form.Database_Check = 'Yes' if request.POST.get('database') == 'on' else 'No'
            bgc_check_form.Reference_Check = 'Yes' if request.POST.get('reference') == 'on' else 'No'
            bgc_check_form.Is_BGC_Check = True
            bgc_check_form.Last_Modified = datetime.datetime.now()
            bgc_check_form.BGC_Status = 'SUBMITTED'
            bgc_check_form.save()
            context['message_bgc'] = 'Data has been Saved !!!'
            obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
            context['obj_bgc'] = obj_bgc
            bgc_check_info = request.POST
            context['bgc_check_info'] = bgc_check_info
            return render(request, 'initiation_form.html', context)
    else:
        context['bgc_check_info'] = request.POST
        return render(request, 'initiation_form.html', context)


def save_vendor(request):
    global obj_bgc
    obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
    context = {
        'obj_location': Location.objects.all(),
        'obj_sub_location': SubLocation.objects.all(),
        'obj_QualificationToHire': QualificationToHire.objects.all(),
        'CC_list': CriticalClient.objects.all(),
        'photo_id_fields': PhotoIDProof.objects.all(),
        'address_proof_fields': AddressProof.objects.all(),
        'obj_bgc': obj_bgc,
        'row_count': 0,
        'VendorList': Vendor.objects.all(),
    }
    if request.method == 'POST' and 'btn_vendor' in request.POST:
        vendor_form = BGCInitiation.objects.get(id=final_bgc_id)
        vendor_form.Vendor_Name = request.POST.get('vendor_name')
        try:
            Initiation_Date = datetime.datetime.strptime(request.POST.get('initiation_date'), '%d-%m-%Y')
        except:
            Initiation_Date = datetime.datetime.strptime(request.POST.get('initiation_date'), '%d-%b-%Y')
        vendor_form.Initiation_Date = Initiation_Date
        vendor_form.Checker_Name = request.user.first_name
        vendor_form.Checker_ID = request.user.username
        vendor_form.Remarks = request.POST.get('vendor_remarks').strip()
        vendor_form.Is_Vendor = True
        vendor_form.Last_Modified = datetime.datetime.now()
        vendor_form.BGC_Status = 'INITIATED'
        # Generate Unique Code
        BGC_Unique_Code = generate_unique_code(id=final_bgc_id, is_drug_test=obj_bgc.Drug_Test,
                                               is_critical_client=obj_bgc.Critical_Client)
        vendor_form.BGC_Unique_Code = BGC_Unique_Code.upper()
        vendor_form.save()
        context['vendor_form_fields'] = VendorFormFields(request.POST)
        context['message_vendor'] = 'Successfully Initiated. BGC Code is ' + BGC_Unique_Code.upper()
        obj_bgc = BGCInitiation.objects.get(id=final_bgc_id)
        context['obj_bgc'] = obj_bgc
        vendor_info = request.POST
        context['vendor_info'] = vendor_info
        return render(request, 'initiation_form.html', context)
    return render(request, 'initiation_form.html', context)
