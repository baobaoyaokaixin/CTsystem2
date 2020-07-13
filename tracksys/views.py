import os

import requests
import urllib3
from PIL import Image
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.views import View
from pymongo import MongoClient
import logging
from django.contrib.auth import logout, settings
import datetime
from tracksys import utils
import pandas as pd
import uuid
from bson import ObjectId

# Create your views here.
from tracksys import verify

client = MongoClient(host=settings.MONGOENGINE['HOST'], port=settings.MONGOENGINE['PORT'])
database = client['CTsystem']
user_collection = database['user_info']
support_admin_collection = database['support_admin']
admin_collection = database['admin_info']
certificate_record_collection = database['certificate_record']
certificate_collection = database['certificate']
training_record_collection = database['training_record']
training_collection = database['training']
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

urllib3.disable_warnings()


def indexView(request):
    title = "User Login"
    return render(request, 'login.html', locals())


# User Login


def UserLogin(request):
    if request.method == 'POST':
        cecid = request.POST['cecid']
        password = request.POST['password']
        request.session['user'] = cecid
        request.session['pass'] = password
        user = verify.backend(cec=cecid, password=password).authenticate()
        user = 1
        if user == 1:
            response = requests.get('https://orgstats.cisco.com/api/1/entries?users=' + cecid)
            message = eval(response.text)
            collection = database['user_info']
            result = list(collection.find({"cecid": cecid}, {"_id": 0}))
            if message:
                firstname = message[0]['N']
                departid = message[0]['O']
                employid = message[0]['i']
                active = message[0]['a']
                if 'r' in message[0]:
                    subordinate = message[0]['r']
                else:
                    subordinate = []
                if active == 1:
                    active = "true"
                else:
                    active = "false"
                title = message[0]['t']
                manager = message[0]['m']
                organazation = message[0]['o']
                if 'C' in message[0]:
                    country = message[0]['C']
                else:
                    country = ""
                if 's' in message[0]:
                    site = message[0]['s']
                else:
                    site = ""
                badge = ''
                if 'R' in message[0]:
                    badge = 'regular_employee'
                elif 'T' in message[0]:
                    badge = 'temp_employee'
                elif 'V' in message[0]:
                    badge = 'vendor'
                dic = {
                    'cecid': cecid,
                    'name': firstname,
                    'gender': "",
                    'title': title,
                    'manager': manager,
                    'subordinate': subordinate,
                    'departid': departid,
                    'employid': employid,
                    'organazation': organazation,
                    'badge': badge,
                    'site': site,
                    'country': country,
                    'active': active,
                }
                if not result:
                    collection.insert_one(dic)
                else:
                    collection.update_one({"cecid": cecid}, {"$set": dic})
                return redirect('tracksys:main')
            else:
                if result:
                    collection.update_one({"cecid": cecid}, {"$set": {"active": 'false'}})
                return render(request, 'login.html',
                              {'error_message': "you don't belong to any group"})
        else:
            error_message = 'Unauthorized, try typing your credentials again'
            return render(request, 'login.html', dict(error_message=error_message))


# User Logout
def user_logout(request):
    logout(request)
    request.session.clear()
    return render(request, 'login.html')


# isLogin
def isLogin(request):
    if request.user == 'AnonymousUser':
        error_message = 'Login Required'
        return render(request, 'login.html', dict(error_message=error_message))
    else:
        pass


# Identity Information
def information(request):
    cecid = request.session['user']
    user_collection = database['user_info']
    admin_collection = database['admin_info']
    support_admin_collection = database['support_admin']
    userinfo = list(user_collection.find({'cecid': cecid}, {'_id': 0}))[0]
    admininfo = list(admin_collection.find({'cecid': cecid, 'active': "true"}, {'_id': 0}))
    support_admin = list(support_admin_collection.find({'cecid': cecid, 'active': "true"}, {'_id': 0}))
    p_admin = c_admin = 0
    if userinfo.get('subordinate'):
        mgr = 1
    else:
        mgr = 0
    if support_admin:
        support_admin = support_admin[0]
        AA = 1
        mgr = 1
    else:
        AA = 0
    if admininfo:
        admininfo = admininfo[0]
        if 'people_admin' in admininfo.get('type'):
            p_admin = 1
        if 'certificate_admin' in admininfo.get('type'):
            c_admin = 1
    return p_admin, c_admin, AA, mgr, support_admin, userinfo


# Main page

def main(request):
    if request.method == 'GET':
        isLogin(request)
        p_admin, c_admin, AA, mgr, support_admin, user = information(request)
        title = 'User'
        cecid = request.session['user']
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        certificate_record = list(
            certificate_record_collection.find({"cecid": cecid, "certificate_info.status": "true"}, {'_id': 0}))
        training_record = list(
            training_record_collection.find({"cecid": cecid, "certificate_info.status": "true"}, {'_id': 0}))
        if certificate_record:
            certificate_record = certificate_record[0]
        if training_record:
            training_record = training_record[0]
        return render(request, 'user_view.html', locals())


def managerView(request):
    if request.method == 'GET':
        isLogin(request)
        p_admin, c_admin, AA, mgr, support_admin, user = information(request)
        cecid = request.session['user']
        user_collection = database['user_info']
        ops_team = database['ops_team']
        title = "Manager"
        if AA:
            if list(ops_team.find({"cecid": cecid, "active": "true"}, {"_id": 0})):
                mgrid = list(ops_team.find({"cecid": cecid, "active": "true"}, {"_id": 0}))[0].get("belongs_to")
            else:
                mgrid = user.get('manager')
            manager = list(user_collection.find({'cecid': mgrid, 'active': "true"}, {'_id': 0}))[0]
            subordinate = manager.get('subordinate', [])
        else:
            mgrid = cecid
            subordinate = user.get('subordinate', [])
        manager_list = []
        none_manager_list = []
        print(subordinate)
        for i in subordinate:
            # utils.get_user_info(i)
            temp = list(user_collection.find({'cecid': i, 'active': "true"}, {'_id': 0}))[0]
            if temp.get('subordinate'):
                manager_list.append(temp)
            else:
                none_manager_list.append(temp)
        mgrs = list(user_collection.find({"subordinate": {"$ne": []}}, {'_id': 0}))
        return render(request, 'manager_view.html', locals())


def get_subordinate(request):
    cecid = request.GET.get('mgrid')
    user_collection = database['user_info']
    user = list(user_collection.find({'cecid': cecid, 'active': "true"}, {'_id': 0}))[0]
    subordinate = user.get('subordinate', [])
    manager_list = []
    none_manager_list = []
    for i in subordinate:
        # utils.get_user_info_simple(i)
        temp = list(user_collection.find({'cecid': i, 'active': "true"}, {'_id': 0}))[0]
        if temp.get('subordinate'):
            manager_list.append(temp)
        else:
            none_manager_list.append(temp)
    data = {
        'mgrid': cecid,
        'manager_list': manager_list,
        'none_manager_list': none_manager_list,
    }
    return JsonResponse(data, safe=False)


# Click User View

def user_view(request, cid):
    isLogin(request)
    title = 'User'
    cecid = cid
    user_collection = database['user_info']
    user = list(user_collection.find({'cecid': cecid, 'active': "true"}, {'_id': 0}))[0]
    certificate_record_collection = database['certificate_record']
    training_record_collection = database['training_record']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    certificate_record = list(certificate_record_collection.find({"cecid": cecid, "status": "true"}, {}))
    training_record = list(training_record_collection.find({"cecid": cecid, "status": "true"}, {}))
    if certificate_record:
        for i in certificate_record:
            i['_id'] = str(i['_id'])
    if training_record:
        for i in training_record:
            i['_id'] = str(i['_id'])
    return render(request, 'user_view_others.html', locals())


def peopleAdminView(request):
    pass


def certificateAdminView(request):
    pass


def trackReport(request):
    isLogin(request),
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    title = "Track Report"
    cecid = request.session['user']
    ops_team = database['ops_team']
    if list(ops_team.find({"cecid": cecid, "active": "true"}, {"_id": 0})):
        manager = list(ops_team.find({"cecid": cecid, "active": "true"}, {"_id": 0}))[0].get("belongs_to")
    else:
        manager = user.get('manager')
    regions = list(
        user_collection.distinct("organazation", {"title": "TECHNICAL CONSULTING ENGINEER.CUSTOMER DELIVERY"}))
    titles = list(user_collection.distinct("title"))
    service_type = ['Proactive Services', 'Support Services']
    total_count = len(list(database['certificate_record'].find({"status": "true"}, {"_id": 0})))
    ccie_count = 0
    ccie_list = []
    reportline = support_admin.get('reportline')
    bluebadge_count = utils.getBadge(reportline).get('bluebadge_count')
    for i in reportline:
        temp = list(certificate_record_collection.find({"cecid": i}, {'_id': 0}))
        if temp:
            temp = temp[0].get('certificate_info', [])
            for j in temp:
                if j.get("status") == "true" and j.get('certificate_type') == "CCIE":
                    ccie_list.append(j)
    ccie_count = len(ccie_list)
    return render(request, 'charts.html', locals())


def analyseReport(request):
    isLogin(request)
    region = request.GET.get("region", "")
    title = request.GET.get("title", "")
    service_type = request.GET.get("service_type", "")
    mgrid = request.GET.get("mgrid", "")
    cecid = request.session.get("user")
    filter_dic = {'active': "true", "title": title, "organazation": region}
    if title == 'All':
        filter_dic.pop("title")
    if region == 'All':
        filter_dic.pop("organazation")
    if service_type == 'All':
        pass
    reportline = []
    users = list(support_admin_collection.find({'cecid': cecid, 'active': "true"}, {'_id': 0}))[0]['reportline']
    filter_users = list(user_collection.find(filter_dic, {'_id': 0}))
    for i in filter_users:
        if i.get('cecid') in users:
            reportline.append(i.get('cecid'))
    total_count = len(reportline)
    ccie_list = []
    for i in reportline:
        temp = list(certificate_record_collection.find({"cecid": i}, {'_id': 0}))
        if temp:
            temp = temp[0].get('certificate_info', [])
            for j in temp:
                if j.get("status") == "true" and j.get('certificate_type') == "CCIE":
                    ccie_list.append(j)
    ccie_count = len(ccie_list)
    bluebadge_count = utils.getBadge(reportline).get("bluebadge_count")
    data = dict(total_count=total_count, bluebadge_count=bluebadge_count,
                ccie_count=ccie_count, ccie_list=ccie_list, reportline=reportline)
    return JsonResponse(data=data, safe=False)


def downloadReport(request):
    cecid = request.session['user']
    reportline = request.GET.get('reportline')
    if not reportline:
        reportline = list(support_admin_collection.find({"cecid": cecid, "active": "true"}, {'_id': 0}))[0].get(
            'reportline')
    filename = cecid + 'AnalysisReport.xlsx'
    path = settings.REPORTFILES_ROOT
    info_lst = []
    for i in reportline:
        user = list(user_collection.find({'cecid': i, 'active': "true"}, {'_id': 0}))[0]
        certificate_record = list(
            certificate_record_collection.find({'cecid': i}, {'_id': 0}))
        if not certificate_record:
            dic = {
                "cecid": user.get('cecid'),
                "name": user.get('name'),
                "title": user.get('title'),
                "region": user.get('organazation'),
                "badge": user.get('badge'),
                "certificate_name": "",
                "certificate_type": "",
                "exam_date": "",
                "score_date": "",
            }
            info_lst.append(dic)
        else:
            certificate_record = certificate_record[0].get('certificate_info')
            for j in certificate_record:
                if j.get('status') == "true":
                    dic = {
                        "cecid": user.get('cecid'),
                        "name": user.get('name'),
                        "title": user.get('title'),
                        "region": user.get('organazation'),
                        "badge": user.get('badge'),
                        "certificate_record": j
                    }
                    dic.update(dic.pop('certificate_record'))
                    dic.pop('uuid')
                    dic.pop('evidence')
                    dic.pop('status')
                    info_lst.append(dic)
                else:
                    continue
    pf = pd.DataFrame(info_lst)
    private_path = os.path.join(path, cecid)
    if not os.path.exists(private_path):
        os.makedirs(private_path)
    pf.to_excel(os.path.join(private_path, filename))
    file = open(os.path.join(private_path, filename), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + filename
    return response


# Get Add Record Page

def get_add_certificate_record_page(request):
    title = "Add Certificate Record "
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    cecid = request.session['user']
    certificate_type = list(certificate_collection.distinct("certificate_type"))
    certificate_type.append("Other Certificate")
    return render(request, 'add_cert.html', locals())


# Get Certificate Name

def get_certificate_name(request):
    certificate_type = request.GET.get('cert_type')
    certificate_name = list(certificate_collection.find({"certificate_type": certificate_type}, {'_id': 0,
                                                                                                 "certificate_name": 1}))
    data = certificate_name
    return JsonResponse(data=data, safe=False)


# Add Certificate Record

def add_certificate_record(request):
    cecid = request.session.get('user')
    certificate_type = request.POST.get("certificate_type", "")
    certificate_name = request.POST.get("certificate_name", "").strip()
    others = request.POST.get("certificate_others", "").strip()
    exam_date = request.POST.get("exam_date", "")
    score_date = request.POST.get("score_date", "")
    description = request.POST.get("description", "")
    files = request.FILES.getlist("upload", [])
    record = list(certificate_record_collection.find({'cecid': cecid}, {'_id': 0}))
    flist = []
    if files:
        for i in files:
            type = i.name.split('.')[1]
            time = datetime.datetime.now()
            time = str(time)
            a = time[:4] + time[5:7] + time[8:10] + time[11:13] + time[14:16] + time[17:19] + time[20:26]
            upfilesave = '%s/%s%s.%s' % (
                settings.UPLOADFILES_ROOT, certificate_name, a, type)
            savefile = '%s/%s' % (settings.UPLOADFILES_ROOT, cecid)
            try:
                img = Image.open(i)
                img.save(upfilesave)
            except IOError as e:
                os.makedirs(savefile)
                img = Image.open(i)
                img.save(upfilesave)
            flist.append(upfilesave)
    if certificate_name:
        certificate_name = certificate_name
    else:
        certificate_name = others
    if record:
        certificate_record_collection.update({'cecid': cecid}, {'$push':
            {'certificate_info':
                {
                    'create_time': timestamp,
                    'certificate_name': certificate_name,
                    'certificate_type': certificate_type,
                    'exam_date': exam_date,
                    'score_date': score_date,
                    'description': description,
                    'status': 'true',
                    'uuid': str(uuid.uuid4()),
                    'evidence': flist
                }
            }})
    else:
        certificate_record_collection.insert(
            {
                'cecid': cecid,
                'certificate_info': [{

                    'create_time': timestamp,
                    'certificate_name': certificate_name,
                    'certificate_type': certificate_type,
                    'exam_date': exam_date,
                    'score_date': score_date,
                    'description': description,
                    'status': 'true',
                    "uuid": str(uuid.uuid4()),
                    'evidence': flist

                }]})
    return redirect('tracksys:main')


# Get Add Record Page

def get_edit_certificate_record_page(request, cid):
    title = "Edit Certificate Record "
    uuid = cid
    cecid = request.session.get('user')
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    certificate_type = list(certificate_collection.distinct("certificate_type"))
    certificate_type.append("Other Certificate")
    certificate_record = list(
        certificate_record_collection.find({"cecid": cecid}, {"_id": 0, 'cecid': 0}))[0].get('certificate_info')
    for i in certificate_record:
        if i.get('uuid') == uuid:
            certificate_record = i
            break
    return render(request, 'edit_cert.html', locals())


# Edit Certificate Record

def edit_certificate_record(request):
    cecid = request.session.get('user')
    certificate_type = request.POST.get("certificate_type", "")
    certificate_name = request.POST.get("certificate_name", "").strip()
    others = request.POST.get("certificate_others", "").strip()
    exam_date = request.POST.get("exam_date", "")
    score_date = request.POST.get("score_date", "")
    description = request.POST.get("description", "")
    files = request.FILES.getlist("upload", [])
    uuid = request.POST.get("uuid")
    flist = []
    if files:
        for i in files:
            type = i.name.split('.')[1]
            time = datetime.datetime.now()
            time = str(time)
            a = time[:4] + time[5:7] + time[8:10] + time[11:13] + time[14:16] + time[17:19] + time[20:26]
            upfilesave = '%s/%s%s.%s' % (
                settings.UPLOADFILES_ROOT, certificate_name, a, type)
            savefile = '%s/%s' % (settings.UPLOADFILES_ROOT, cecid)
            try:
                img = Image.open(i)
                img.save(upfilesave)
            except IOError as e:
                os.makedirs(savefile)
                img = Image.open(i)
                img.save(upfilesave)
            flist.append(upfilesave)
    if certificate_name:
        certificate_name = certificate_name
    else:
        certificate_name = others

    certificate_record_collection.update_one({'cecid': cecid}, {'$set':
        {'certificate_info.$[c]':
            {
                'create_time': timestamp,
                'certificate_name': certificate_name,
                'certificate_type': certificate_type,
                'exam_date': exam_date,
                'score_date': score_date,
                'description': description,
                'status': 'true',
                'uuid': uuid,
                'evidence': flist
            }
        }}, upsert=False, array_filters=[{'c.uuid': uuid}])
    return redirect('tracksys:main')


# Delete Certificate Record
def delete_certificate_record(request, cid):
    cecid = request.session.get('user')
    certificate_record_collection.update_one({'cecid': cecid}, {'$set':
                                                                    {'certificate_info.$[c].status': "false"
                                                                     }}, upsert=False, array_filters=[{'c.uuid': cid}])
    return redirect('tracksys:main')


# Add Training Record

def add_training_record(args):
    pass


# Edit Training Record

def edit_training_record(args):
    pass


# Delete Training Record
def delete_training_record(args):
    pass


# View Detail
def view_certificate_detail(request, cid):
    cecid = request.session.get('user')
    uuid = cid
    title = "Certificate Record Detail"
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    certificate_record = list(
        certificate_record_collection.find({"cecid": cecid}, {"_id": 0, 'cecid': 0}))[0].get('certificate_info')
    for i in certificate_record:
        if i.get('uuid') == uuid:
            certificate_record = i
    certificate = \
        list(
            certificate_collection.find({"certificate_type": certificate_record['certificate_type'], "certificate_name":
                certificate_record['certificate_name']}, {"_id": 0}))[0]
    evidence = []
    certificate_record.update(certificate)
    for i in certificate_record.get('evidence'):
        i = i.split("/")[-1]
        evidence.append(i)
    certificate_record['evidence'] = evidence
    return render(request, 'certificate_record_detail.html', locals())


def view_training_detail():
    pass


# Admin

def get_cert_admin_page(request):
    title = "Certificate Admin"
    cecid = request.session.get('user')
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    certificates = list(certificate_collection.find({}))
    for i in certificates:
        i["id"] = str(i["_id"])
        i.pop("_id")
    certificate_type = list(certificate_collection.distinct("certificate_type"))
    return render(request, 'cert_admin_view.html', locals())


def cert_type(request):
    cert_type = request.GET.get("cert_type")
    title = "Certificate Admin"
    cecid = request.session.get('user')
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    certificates = list(certificate_collection.find({"certificate_type": cert_type}, {"_id": 0}))
    certificate_type = list(certificate_collection.distinct("certificate_type"))
    return render(request, 'cert_admin_view.html', locals())


def add_cert_info_page(request):
    title = "Add Certificate Information"
    cecid = request.session.get('user')
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    certificate_type = list(certificate_collection.distinct("certificate_type"))
    certificate_type.append("Other Certificate")
    print(certificate_type)
    return render(request, 'add_cert._admin.html', locals())


def add_cert_info(request):
    cecid = request.session.get('user')
    certificate_name = request.POST.get('certificate_name')
    certificate_type = request.POST.get('certificate_type')
    active_duration = request.POST.get('active_duration', "")
    description = request.POST.get('description', "")
    priority = request.POST.get('priority', "")
    edit_by = cecid
    print(priority, certificate_name, certificate_type)
    certificate_collection.insert_one({
        "certificate_name": certificate_name,
        "certificate_type": certificate_type,
        "active_duration": str(active_duration) + "days",
        "description": description,
        "priority": priority,
        "edit_by": edit_by,
        "delete_by": "",

    })
    return redirect('tracksys:certAdminPage')


def edit_cert_info_page(request, cid):
    cecid = request.session.get('user')
    title = "Edit Certificate information"
    p_admin, c_admin, AA, mgr, support_admin, user = information(request)
    cert = list(certificate_collection.find({"_id": ObjectId(cid)}, {"_id": 0}))[0]
    return render(request, 'edit_cert_admin.html', locals())


def edit_cert_info(request):
    cecid = request.session.get('user')
    certificate_name = request.POST.get('certificate_name')
    certificate_type = request.POST.get('certificate_type')
    active_duration = request.POST.get('active_duration', "")
    description = request.POST.get('description', "")
    priority = request.POST.get('priority', "")
    status = request.POST.get('status', "")
    edit_by = cecid
    if status == "true":
        delete_by = ""
    else:
        delete_by = cecid
    certificate_collection.insert_one({
        "certificate_name": certificate_name,
        "certificate_type": certificate_type,
        "active_duration": str(active_duration) + "days",
        "description": description,
        "priority": priority,
        "edit_by": edit_by,
        "status":status,
        "delete_by": delete_by,

    })
    return redirect('tracksys:certAdminPage')


def groupSummary(request):
    mgrid = request.GET.get('mgrid')
    mcount = utils.getReportline(mgrid).get('total_count')
    reportline = utils.getReportline(mgrid).get(mgrid)
    ccie_list = []
    for i in reportline:
        temp = list(certificate_record_collection.find({"cecid": i}, {'_id': 0}))
        if temp:
            temp = temp[0].get('certificate_info', [])
            for j in temp:
                if j.get("status") == "true" and j.get('certificate_type') == "CCIE":
                    ccie_list.append(j)
    ccie_count = len(ccie_list)
    data = {
        'mcount': mcount,
        'count': ccie_count
    }
    return JsonResponse(data=data, safe=False)
