from django.db import models
import mongoengine

# Create your models here.

# userinfo
user_dic = {
    'cecid': 'cecid',
    'name': 'firstname',
    'gender': "",
    'title': 'title',
    'manager': 'manager',
    'subordinate': [],
    'departid': 'departid',
    'employid': 'employid',
    'organazation': 'organazation',
    'site': 'site',
    'country': 'country',
    'active': 'active',
    'badge': '',
}

# admininfo
admin_dic = {
    'cecid': '',
    'type': [],
    'active': '',
    'create_by': '',
}
# certificate_record
cert_record = {
    "cecid": "",
    "certificate_info": [{
        'create_time': '',
        'certificate_name': '',
        'certificate_type': '',
        'exam_date': '',
        'score_date': '',
        'description': '',
        'status': '',
        'evidence': []
    }]

}
# training_record
training_record = {
    "cecid": "",
    "training_info": [{
        'create_time': '',
        'training_name': '',
        'training_type': '',
        'start_date': '',
        'end_date': '',
        'description': '',
        'status': '',
        'evidence': [],
        'exam': [{
            'name': '',
            'date': '',
            'score': '',
        }]
    }]

}

# certificate
certificate = {
    "certificate_name": "",
    "certificate_type": "",
    "active_duration": "",
    "description": '',
    "priority": "",
    "edit_by": "",
    "delete_by": "",

}

# training
training = {
    "training_name": "",
    "training_type": "",
    "description": '',
    "priority": "",
    "edit_by": "",
    "delete_by": "",
}

super_admin = {
    "cecid": "",
}

support_admin = {
    "cecid": "",
    "active": ""
}
ops_team_ = {
    "cecid": "",
    "active": "",
    "belongs_to": ""
}
