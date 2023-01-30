import json

import unidecode
import xmltodict
import requests
import re
from django.contrib.auth.models import User, Group
from electronicSignature import settings
from main.models.address import Address
from main.models.address_type import AddressType
from main.models.company import Company
from main.models.entity import EntityPhone, EntityAddress
from main.models.formationsession import Objectifs_peda
from main.models.person import Person
from main.models.phone import Phone


def GetAuthToken():
    apiUsername = settings.API_USER
    apiPsswd = settings.API_PSSWD
    baseUrl = "https://www.cirrus-shield.net/RestApi/AuthToken?Username="
    callUrl = baseUrl + apiUsername + "&password=" + apiPsswd
    response = requests.get(callUrl)
    authToken = response.text
    return authToken


def GetFormationSession(formation_id):
    search_result = {}

    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    num_dossier = formation_id
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Name,Id,CreationDate,Annee_du_contrat,Commercial_principal,Client_Account," \
                  "Number_of_Trainees,,Formation_a_distance_liste," \
                  "Numero_de_la_rue,Rue,Ville_Commune,Code_postal,Training_Offer,Pre_requisites_Verified,Formateur,OPCO," \
                  "Authorized_Start_Date,Authorized_End_Date,Expected_Start_Date,Expected_End_Date," \
                  "Cout_du_formateur,Total_Number_of_Training_Hours," \
                  "+from+Contrat_de_Formation+where+Numero_du_dossier=" \
                  + num_dossier
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS

    # parse the response into dict
    xpars = xmltodict.parse(response.text)

    year = xpars['Data']['Contrat_de_Formation']['Annee_du_contrat']

    # slice the year out of dd/mm/yyyy
    if year != None:
        formatted_year = year[-4:]
    else:
        formatted_year = year

    xpars['Data']['Contrat_de_Formation']['Annee_du_contrat'] = formatted_year
    xpars['success'] = search_was_successful
    tutor_id = xpars['Data']['Contrat_de_Formation']['Formateur']
    xpars['Data']['Contrat_de_Formation']['Formateur'] = getTutor(tutor_id)

    # ugly needs modif 5 ifs..
    if xpars['Data']['Contrat_de_Formation']['Authorized_Start_Date'] != None:
        xpars['Data']['Contrat_de_Formation']['Authorized_Start_Date'] = xpars['Data']['Contrat_de_Formation'][
                                                                             'Authorized_Start_Date'][:10]

    if xpars['Data']['Contrat_de_Formation']['Authorized_End_Date'] != None:
        xpars['Data']['Contrat_de_Formation']['Authorized_End_Date'] = xpars['Data']['Contrat_de_Formation'][
                                                                           'Authorized_End_Date'][:10]

    if xpars['Data']['Contrat_de_Formation']['Expected_Start_Date'] != None:
        xpars['Data']['Contrat_de_Formation']['Expected_Start_Date'] = xpars['Data']['Contrat_de_Formation'][
                                                                           'Expected_Start_Date'][:10]

    if xpars['Data']['Contrat_de_Formation']['Expected_End_Date'] != None:
        xpars['Data']['Contrat_de_Formation']['Expected_End_Date'] = xpars['Data']['Contrat_de_Formation'][
                                                                         'Expected_End_Date'][:10]

    if xpars['Data']['Contrat_de_Formation']['CreationDate'] != None:
        xpars['Data']['Contrat_de_Formation']['CreationDate'] = xpars['Data']['Contrat_de_Formation']['CreationDate'][
                                                                :10]

    session_id = xpars['Data']['Contrat_de_Formation']['Id']
    xpars['Data']['Contrat_de_Formation']['Stagiaires'] = getTrainee(session_id)
    opco = xpars['Data']['Contrat_de_Formation']['OPCO']
    xpars['Data']['Contrat_de_Formation']['OPCO'] = getOpco(opco)
    commercial = xpars['Data']['Contrat_de_Formation']['Commercial_principal']
    xpars['Data']['Contrat_de_Formation']['Commercial_principal'] = getCommercial(commercial)
    client = xpars['Data']['Contrat_de_Formation']['Client_Account']
    foad = xpars['Data']['Contrat_de_Formation']['Formation_a_distance_liste']
    xpars['Data']['Contrat_de_Formation']['Client_Account'] = getClient(client, foad)

    if xpars['Data']['Contrat_de_Formation']['Training_Offer'] != None:
        xpars['Data']['Contrat_de_Formation']['Training_Offer'] = getObjectif(
            xpars['Data']['Contrat_de_Formation']['Training_Offer'])

    if (xpars['Data']['Contrat_de_Formation']['Formation_a_distance_liste'] != "Oui"):
        xpars['Data']['Contrat_de_Formation']['Numero_de_la_rue'] = create_address(
            str(xpars['Data']['Contrat_de_Formation']['Numero_de_la_rue']) + " " +
            str(xpars['Data']['Contrat_de_Formation']['Rue']),
            str(xpars['Data']['Contrat_de_Formation']['Code_postal']),
            str(xpars['Data']['Contrat_de_Formation']['Ville_Commune'])
        )
    else:
        try:
            db_address = Address.objects.get(details="Formation à distance")
        except Address.DoesNotExist:
            db_address = Address.objects.create(details="Formation à distance")
        xpars['Data']['Contrat_de_Formation']['Numero_de_la_rue'] = db_address

    search_result = xpars

    return search_result


def getObjectif(objectif_id):
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Objectif_pedagogique+from+Product+where+Id=" + objectif_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)

    sentences = re.split(r'(\r\n?|\n)+', xpars['Data']['Product']['Objectif_pedagogique'])
    my_objectifs = []
    for objectif in sentences:
        if objectif != "" and objectif != '\n':
            my_objectifs.append(
                Objectifs_peda.objects.create(
                    description=objectif
                )
            )

    return my_objectifs


def getTrainee(session_id):
    final_trainees = []
    list_of_id = []
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Stagiaire+from+Trainee+Where+Contrat_de_Formation=" + session_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    trainees = xpars['Data']['Trainee']
    for trainee in trainees:
        if search_was_successful and trainee != None:
            length = len(trainees)
            if length == 1:
                selectQuery = "&selectQuery=Select+First_Name,Last_Name,Email,Mobile,Fonction_stagiaire+from+Contact+where+Id=" \
                              + trainees['Stagiaire']
            else:
                selectQuery = "&selectQuery=Select+First_Name,Last_Name,Email,Mobile,Fonction_stagiaire+from+Contact+where+Id=" \
                              + trainee['Stagiaire']
            callUrl = url + selectQuery
            response = requests.get(callUrl)
            search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
            xpars = xmltodict.parse(response.text)
            trainee_email = xpars['Data']['Contact']['Email']
            trainee_phone = xpars['Data']['Contact']['Mobile']
            trainee_first_name = xpars['Data']['Contact']['First_Name']
            trainee_last_name = xpars['Data']['Contact']['Last_Name']
            if search_was_successful:
                # hack to make a fake username
                username = str(trainee_last_name + trainee_first_name)
                # remove accents:core_imagefile
                username = unidecode.unidecode(username)
                # replace special chars by '_':
                username = username.translate(
                    {ord(c): "_" for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=+"}
                )
                try:
                    trainee = User.objects.get(
                        first_name=trainee_first_name,last_name=trainee_last_name
                    )

                    user_group = Group.objects.get(name='learner')
                    trainee.groups.add(user_group)
                    trainee.first_name = trainee_first_name
                    trainee.last_name = trainee_last_name
                    trainee.email = trainee_email
                    trainee.username = username
                    trainee.save()

                    if trainee_phone is not None:
                        phone_trainee = Phone.objects.create(phone_number=trainee_phone)
                        phone_trainee.phone_number = phone_trainee.standardize(phone_trainee.phone_number)
                        phone_trainee.save()

                        entity = EntityPhone.objects.create(
                            entity=trainee.person,
                            phone_type=1,
                            phone=phone_trainee,
                        )

                except User.DoesNotExist:
                    trainee_password = User.objects.make_random_password(),
                    trainee = User.objects.create_user(username=username, email=trainee_email,
                                                       password=str(trainee_password))
                    trainee.first_name = trainee_first_name
                    trainee.last_name = trainee_last_name
                    user_group = Group.objects.get(name='learner')
                    trainee.groups.add(user_group)
                    trainee.save()

                final_trainees.append(trainee)
            for trainee in final_trainees:
                if trainee.id not in list_of_id:
                    list_of_id.append(trainee.id)
    result = Person.objects.filter(user_id__in=list_of_id)

    return result


def getTutor(tutor_id):
    tutor = {}
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+First_Name,Last_Name,Email,SIRET_formateur,Raison_sociale_formateur," \
                  "Mobile+from+Tutor+where+Id=" + tutor_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    tutor_first_name = xpars['Data']['Tutor']['First_Name']
    tutor_last_name = xpars['Data']['Tutor']['Last_Name']
    tutor_email = xpars['Data']['Tutor']['Email']
    siret = xpars['Data']['Tutor']['SIRET_formateur']
    raison_sociale = xpars['Data']['Tutor']['Raison_sociale_formateur']
    tutor_mobile = xpars['Data']['Tutor']['Mobile']
    xpars['success'] = search_was_successful
    tutor = xpars
    if search_was_successful:
        # hack to make a fake username
        username = tutor_email.replace("@", "_at_")
        # remove accents:core_imagefile
        username = unidecode.unidecode(username)
        # replace special chars by '_':
        username = username.translate(
            {ord(c): "_" for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=+"}
        )
        try:
            tutor = User.objects.get(
                username=username,
            )
            user_group = Group.objects.get(name='teacher')
            tutor.groups.add(user_group)
            tutor.save()

        except User.DoesNotExist:
            tutor_password = User.objects.make_random_password(),
            tutor = User.objects.create_user(username=username, email=tutor_email, password=str(tutor_password))
            tutor.first_name = tutor_first_name
            tutor.last_name = tutor_last_name
            user_group = Group.objects.get(name='teacher')
            tutor.groups.add(user_group)
            tutor.save()
        try:
            teacher_company = Company.objects.get(contact=tutor)
        except Company.DoesNotExist:

            address_company = Address.objects.create()

            phone_company = Phone.objects.create(phone_number=tutor_mobile)
            phone_company.phone_number = phone_company.standardize(phone_company.phone_number)
            phone_company.save()

            teacher_company = Company.objects.create(raison_sociale=raison_sociale, num_siret=siret, email=tutor_email,
                                                     phone=phone_company, contact=tutor)
            address = EntityAddress.objects.create(entity=teacher_company, address=address_company,
                                                   address_type=AddressType.objects.get(name=2))
            entity = EntityPhone.objects.create(
                entity=tutor.person,
                phone_type=1,
                phone=phone_company,
            )
            teacher_company.adresse = address
            teacher_company.save()

    return tutor


def getOpco(opco_id):
    opco = {}
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Name+from+OPCO+where+Id=" + opco_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    xpars['success'] = search_was_successful

    opco = xpars
    opco_name = xpars['Data']['OPCO']['Name']

    return opco_name


def getCommercial(commercial_id):
    commercial = {}
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Nom_de_famille,Email,Prenom+from+Commercial+where+Id=" + commercial_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    commercial_last_name = xpars['Data']['Commercial']['Nom_de_famille']
    commercial_first_name = xpars['Data']['Commercial']['Prenom']
    commercial_email = xpars['Data']['Commercial']['Email']
    xpars['success'] = search_was_successful
    try:
        commercial = User.objects.get(email=commercial_email)
        user_group = Group.objects.get(name='commercial')
        commercial.groups.add(user_group)
        commercial.save()
    except User.DoesNotExist:
        # hack to make a fake username
        username = commercial_email.replace("@", "_at_")
        # remove accents:core_imagefile
        username = unidecode.unidecode(username)
        # replace special chars by '_':
        username = username.translate(
            {ord(c): "_" for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=+"}
        )
        commercial_password = User.objects.make_random_password(),
        commercial = User.objects.create_user(username=username, email=commercial_email,
                                              password=str(commercial_password))
        commercial.first_name = commercial_first_name
        commercial.last_name = commercial_last_name
        user_group = Group.objects.get(name='commercial')
        commercial.groups.add(user_group)
        commercial.save()

    return commercial


def getClient(client_id, foad):
    client = {}
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Name,Code_APE,Billing_ZIP,Email_1,Nb_d_employes_1,Nom_1,Numero_de_la_rue," \
                  "OPCO,Prenom_1,Billing_Street,Industry,SIRET,Tel_Fixe_1+from+Account+where+Id=" + client_id
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    xpars['success'] = search_was_successful
    client_account_name = xpars['Data']['Account']['Name']
    client_account_ape = xpars['Data']['Account']['Code_APE']
    client_account_billing_zip = xpars['Data']['Account']['Billing_ZIP']
    client_account_email = xpars['Data']['Account']['Email_1']
    client_account_nb_employes = xpars['Data']['Account']['Nb_d_employes_1']
    client_account_Nom = xpars['Data']['Account']['Nom_1']
    client_account_opco = xpars['Data']['Account']['OPCO']
    client_account_prenom = xpars['Data']['Account']['Prenom_1']
    client_account_industry = xpars['Data']['Account']['Industry']
    client_account_siret = xpars['Data']['Account']['SIRET']
    client_account_tel_fixe = xpars['Data']['Account']['Tel_Fixe_1']
    if type(xpars['Data']['Account']['Numero_de_la_rue']) == str:
        client_account_Num_rue = xpars['Data']['Account']['Numero_de_la_rue']
    else:
        client_account_Num_rue = ""
    if type(xpars['Data']['Account']['Billing_Street']) == str:
        client_account_billingstreet = xpars['Data']['Account']['Billing_Street']
    else:
        client_account_billingstreet = ""

    if search_was_successful:

        try:
            client = Company.objects.get(
                name=client_account_name
            )

        except Company.DoesNotExist:
            # hack to make a fake username
            username = client_account_email.replace("@", "_at_")
            # remove accents:core_imagefile
            username = unidecode.unidecode(username)
            # replace special chars by '_':
            username = username.translate(
                {ord(c): "_" for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=+"}
            )
            try:
                representant_company = User.objects.get(
                    username=username,
                )

            except User.DoesNotExist:
                representant_company_psswd = User.objects.make_random_password(),
                representant_company = User.objects.create_user(username=username, email=client_account_email,
                                                                password=str(representant_company_psswd))
                representant_company.first_name = client_account_prenom
                representant_company.last_name = client_account_Nom
                user_group = Group.objects.get(name='representant_company')
                representant_company.groups.add(user_group)
                representant_company.save()

            phone_company = Phone.objects.create(phone_number=client_account_tel_fixe)
            phone_company.phone_number = phone_company.standardize(phone_company.phone_number)
            phone_company.save()
            client = Company.objects.create(name=client_account_name, code_ape=client_account_ape,
                                            email=client_account_email, numb_employees=client_account_nb_employes[-1],
                                            Industry=client_account_industry, num_siret=client_account_siret,
                                            contact=representant_company, phone=phone_company)
            if type(client_account_billingstreet) != str or type(client_account_Num_rue) != str:
                address_company = Address.objects.create(details=client_account_Num_rue + client_account_billingstreet,
                                                         postal_code=client_account_billing_zip)

                address = EntityAddress.objects.create(entity=client, address=address_company,
                                                       address_type=AddressType.objects.get(name=2))
                client.adresse = address

                client.save()

    else:
        print("can't find tutor")

    return client


def create_address(address_text, postal_code, id_commune):
    authToken = GetAuthToken()
    authToken = authToken.replace('"', '')
    url = "https://www.cirrus-shield.net/RestApi/Query?authToken=" + authToken
    selectQuery = "&selectQuery=Select+Name+from+Ville+where+Id=" + id_commune
    callUrl = url + selectQuery
    response = requests.get(callUrl)
    search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    xpars = xmltodict.parse(response.text)
    if type(address_text) == str:
        address_text = address_text + ", " + str(xpars['Data']['Ville']['Name'])
    else:
        address_text = str(xpars['Data']['Ville']['Name'])
        postal_code = "00000"
    try:
        db_address = Address.objects.get(details=address_text)
    except Address.DoesNotExist:
        db_address = Address.objects.create(details=address_text, postal_code=postal_code)

    return db_address
