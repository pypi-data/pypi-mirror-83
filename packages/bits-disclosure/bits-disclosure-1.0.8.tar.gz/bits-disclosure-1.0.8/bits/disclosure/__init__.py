# -*- coding: utf-8 -*-
"""Disclosure class file."""

import datetime
import time

from bits.mongo import Mongo
# from bits.progressbar import Progress


class Disclosure(Mongo):
    """Disclosure class definition."""

    def __init__(self, mongo_uri, mongo_db, verbose=True):
        """Initialize a class instance."""
        Mongo.__init__(self, mongo_uri, mongo_db, verbose=verbose)
        self.people = {}
        self.responses = {}
        self.users = {}

        self.emaildb = self.db['email']
        self.keyworddb = self.db['keyword']
        self.peopledb = self.db['person']
        self.responsedb = self.db['response']
        self.usersdb = self.db['user']

    def getCollectionsReport(self):
        """Return a report of MongoDB collections."""
        output = []
        collections = [
            'email',
            'keyword',
            'person',
            'response',
            'session',
            'user',
        ]
        for c in collections:
            output.append(str(self.db[c].count())+' '+c)
        return output

    def getEmailTemplates(self):
        """Return a dict of email templates."""
        emails = {}
        for e in self.emaildb.find():
            key = e['_id']
            emails[key] = e
        return emails

    def getKeywords(self):
        """Return a dict of keywords."""
        keywords = {}
        for k in self.keyworddb.find().sort('name'):
            key = k['_id']
            keywords[key] = k
        return keywords

    def getNagCandidates(self):
        """Return a list of candidates to nag."""
        return self.peopledb.find({
            'terminated': False,
            'future_hire': '0',
            'status': 'incomplete',
        }).sort([('date_due', 1), ('first_name', 1), ('last_name', 1)])

    def getPeople(self):
        """Return a dict of people."""
        people = {}
        for p in self.peopledb.find():
            pid = p['pid']
            people[pid] = p
        self.people = people
        return self.people

    def getResponses(self):
        """Return a dict of responses."""
        responses = {}
        for r in self.responsedb.find():
            pid = r['pid']
            if pid in responses:
                responses[pid].append(r)
            else:
                responses[pid] = [r]
        self.responses = responses
        return self.responses

    def getUsers(self):
        """Return a dict of users."""
        users = {}
        for u in self.usersdb.find():
            email = u['email']
            users[email] = u
        self.users = users
        return self.users

    def addMissingPeople(self, missing):
        """Add missing people to the database."""
        for p in sorted(missing, key=lambda x: x['full_name']):
            person = self.preparePerson(p)
            self.peopledb.insert_one(person)
        print

    def missingPeople(self, disclosure_people, people):
        """Return a list of missing people."""
        missing = []
        for pid in people:
            d = people[pid]
            if str(pid) not in disclosure_people:
                missing.append(d)
        return missing

    def removeUnknownPeople(self, unknown):
        """Remove unknown people from the database."""
        for u in sorted(unknown, key=lambda x: x['full_name']):
            _id = u['_id']
            pid = u['pid']
            full_name = str(u['full_name'])
            email = str(u['email'])
            print('   Deleting person '+full_name+' <'+email+'> ['+str(pid)+']')
            self.peopledb.delete_one({'_id': _id})
        print

    def removeUnknownResponses(self, unknown):
        """Remove unknown responses from database."""
        for pid in unknown:
            responses = unknown[pid]
            print('   Deleting responses for: '+str(pid))
            for r in responses:
                _id = r['_id']
                print('     * response: '+str(_id))
                self.responsedb.delete_one({'_id': _id})
            print

    # def removeUnknownUsers(self, unknown):
    #     """Remove unknown users from database."""
    #     for u in sorted(unknown, key=lambda x: x['name']):
    #         uid = u['_id']
    #         name = str(u['name'].encode('ascii', 'ignore'))
    #         email = str(u['email'])
    #         print('   Deleting user '+name+' <'+email+'> ['+uid+']')
    #         self.usersdb.delete_one({'_id': uid})
    #     print

    def unknownPeople(self, disclosure_people, people):
        """Return a list of unknown people."""
        unknown = []
        for pid in disclosure_people:
            d = disclosure_people[pid]
            if int(pid) not in people:
                unknown.append(d)
        return unknown

    def unknownResponses(self, responses, people):
        """Return a dict of unknown responses."""
        unknown = {}
        for pid in responses:
            r = responses[pid]
            if pid and int(pid) not in people:
                unknown[pid] = r
        return unknown

    # def unknownUsers(self, disclosure_users, google_users):
    #     """Return a list of unknown users."""
    #     unknown = []
    #     for email in disclosure_users:
    #         d = disclosure_users[email]
    #         uid = d['_id']
    #         if uid not in google_users:
    #             unknown.append(d)
    #     return unknown

    def preparePerson(self, p):
        """Prepare a person record for the database."""
        # update attributes
        p['ccure_person_id'] = None

        # check pid
        p['pid'] = p.get('id', 0)

        p['short_org_unit'] = p['org_unit'].split(' > ')[-1]
        if p['username']:
            p['email'] = p['username']+'@broadinstitute.org'

        # delete unused attributes
        del p['_id']
        if "adp_sync_date" in p:
            del p['adp_sync_date']
        if "id" in p:
            del p['id']
        if "person_type" in p:
            del p['person_type']

        # check for future hire
        today = datetime.date.today().strftime('%Y-%m-%d')
        p['future_hire'] = '0'
        if p['start_date'] > today:
            p['future_hire'] = '1'

        # set start date
        start_date = datetime.datetime.strptime('1970-01-01', "%Y-%m-%d")
        if p['start_date']:
            start_date = datetime.datetime.strptime(p['start_date'], "%Y-%m-%d")

        # set end date and terminated
        end_date = datetime.datetime.strptime('2999-12-31', "%Y-%m-%d")
        if p['end_date'] and p['end_date'] < today:
            end_date = datetime.datetime.strptime(p['end_date'], "%Y-%m-%d")
            p['terminated'] = True
            p['tenure'] = round(abs(end_date - start_date).days / 365.25, 1)
        else:
            p['terminated'] = False
            p['tenure'] = round(abs(datetime.datetime.today() - start_date).days / 365.25, 1)

        # fix strings:
        for k in p:
            if k in [
                'ccure_person_id',
                'emplid',
                'empl_supervisor_emplid',
                'empl_supervisor_id',
                'has_username',
                'last_updated',
                'mgr_override_id',
                'mgr_override_emplid',
                'nocoi',
                'nohst',
                'nologin',
                'nopass',
                'person_type_id',
                'pid',
                'proxy_emplid',
                'proxy_id',
                'reports_to_emplid',
                'reports_to_id',
                'requestor_emplid',
                'requestor_id',
                'reviewer_emplid',
                'reviewer_id',
                'supervisor_emplid',
                'supervisor_id',
                'tenure',
                'updated',
            ] and p[k] is not None:
                p[k] = str(p[k])

        return p

    def prepareUser(self, g, p=None):
        """Prepare a user record for the database."""
        # get person id
        pid = None
        if p:
            pid = str(p['id'])

        user = {
            'email': g['primaryEmail'],
            'family_name': g['name']['familyName'],
            'given_name': g['name']['givenName'],
            'hd': 'broadinstitute.org',
            'name': g['name']['fullName'],
            'pid': pid,
            'verified_email': True,
        }
        return user

    def comparePerson(self, d, p):
        """Return any updates for a person record."""
        output = []
        update = False
        for k in sorted(p):
            if k not in d:
                d[k] = None
            if d[k] != p[k]:
                if k not in ['last_updated']:
                    update = True
                    output.append(k+': '+str(d[k])+' -> '+str(p[k]))
        if output:
            print('   Updating person: '+p['full_name'])
            print('     * '+'\n     * '.join(output))
            print

        return update

    def compareUser(self, d, g):
        """Return any updates for a user record."""
        output = []
        for k in sorted(g):
            if k not in d:
                d[k] = None
            if d[k] != g[k]:
                try:
                    output.append(k+': '+str(d[k])+' -> '+str(g[k]))
                except Exception:
                    output.append(k+': '+str(d[k].encode('ascii', 'ignore'))+' -> '+str(g[k]))
        if output:
            print('   Updating user: '+g['name'])
            print('     * '+'\n     * '.join(output))
            print

        return output

    def updateDueDates(self):
        """Update due dates in the database."""
        for p in self.peopledb.find().sort('start_date'):
            start_due = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
            if p['start_date']:
                start_due = datetime.datetime.strptime(p['start_date'], '%Y-%m-%d') + datetime.timedelta(days=14)

            # fix string date_due to datetime
            if 'date_due' in p and isinstance(p['date_due'], str):
                print('Updating str date to datetime: {}'.format(p['date_due']))
                p['date_due'] = datetime.datetime.strptime(p['date_due'][:10], '%Y-%m-%d')
                self.updatePerson(p)

            # due date is set to something before start due date
            if 'date_due' in p and p['date_due'] < start_due:
                print('   Updating due date for '+p['full_name']+' from '+str(p['date_due'])[:10]+' to '+str(start_due)[:10]+'.')
                print('   * start_date: '+str(p['start_date']))
                p['date_due'] = start_due
                self.updatePerson(p)

            # due date is not set to anything
            elif 'date_due' not in p:
                print('   Setting due date for '+p['full_name']+' to '+str(start_due)+'.')
                p['date_due'] = start_due
                self.updatePerson(p)

    def updateStatuses(self):
        """Update statuses in the database."""
        cutoff = datetime.datetime.now() + datetime.timedelta(days=30)
        for p in self.peopledb.find({'terminated': False}).sort('date_due', 1):

            # status not yet set
            if 'status' not in p:

                # due in the next 30 days or earlier
                if p['date_due'] < cutoff:
                    print('   Setting status to incomplete for '+p['full_name']+' due on '+str(p['date_due']))
                    p['status'] = 'incomplete'
                    self.updatePerson(p)

                # due date is more than 30 days in the future
                else:
                    print('   Setting status to completed for '+p['full_name']+' due on '+str(p['date_due']))
                    p['status'] = 'completed'
                    self.updatePerson(p)

            # status is already set to something
            else:

                # skip updating the status for anyone who is excluded
                if p['status'] == 'exempt':
                    # print('Skipping exempt person: '+p['full_name'])
                    continue

                # due date is in the next 30 days or earlier and status is not incomplete
                if p['date_due'] < cutoff and p['status'] != 'incomplete':
                    print('   Updating status to incomplete for '+p['full_name']+' due on '+str(p['date_due']))
                    p['status'] = 'incomplete'
                    self.updatePerson(p)

                # due date is more than 30 days in the future and status is incomplete
                elif p['date_due'] > cutoff and p['status'] == 'incomplete':
                    print('   Updating status to completed for '+p['full_name']+' due on '+str(p['date_due']))
                    p['status'] = 'completed'
                    self.updatePerson(p)

    def updatePerson(self, person):
        """Update a person in the database."""
        pid = person['pid']

        # get current record
        current = self.peopledb.find_one({'pid': str(pid)})
        if not current:
            print('Person not found! '+str(pid))
            return

        new = dict(current)
        for key in person:
            new[key] = person[key]

        print('Updating {}...'.format(pid))
        self.peopledb.replace_one({'pid': str(pid)}, new)

    def updatePeople(self, disclosure_people, people):
        """Update people in the database."""
        count = 0
        for pid in sorted(disclosure_people, key=lambda x: disclosure_people[x]['full_name']):
            d = disclosure_people[pid]
            if int(pid) not in people:
                print('Person not found: '+pid)
                continue
            p = self.preparePerson(people[int(pid)])
            update = self.comparePerson(d, p)
            if update:
                count += 1
                self.updatePerson(p)
        return count

    def updateUser(self, user):
        """Update a user in the database."""
        # uid = user['_id']
        email = user['email']
        current = self.usersdb.find_one({'email': email})
        if not current:
            print('User not found! %s' % (email))
            return

        for key in user:
            current[key] = user[key]

        self.usersdb.replace_one({'email': email}, current)

    def updateUsers(self, disclosure_users, google_users, people):
        """Update users in the database."""
        count = 0

        # get users to add
        add = []
        for email in sorted(google_users):
            if email not in disclosure_users:
                add.append(google_users[email])
        if add:
            print('Never logged in: %s' % (len(add)))

        # get users to delete
        delete = []
        for email in sorted(disclosure_users):
            if email not in google_users:
                delete.append(email)
        if delete:
            print('Users to delete: %s' % (len(delete)))
            for email in sorted(delete):
                print('Deleting user: %s' % (email))
                self.usersdb.delete_one({'email': email})

        # get users to update
        for email in sorted(google_users):
            if email not in disclosure_users:
                continue
            disclosure_user = dict(disclosure_users[email])
            google_user = self.prepareUser(google_users[email], people.get(email))

            # delete unchecked keys
            unchecked = [
                '_id',
                '_count',
                'createdAt',
                'gender',
                'link',
                'locale',
                'picture',
                'role',
                'updatedAt',
            ]
            for key in unchecked:
                if key in disclosure_user:
                    del disclosure_user[key]

            if disclosure_user != google_user:
                print('Update User: %s' % (email))
                for key in set(list(disclosure_user) + list(google_user)):
                    d = disclosure_user.get(key)
                    g = google_user.get(key)
                    if d != g:
                        print('   * %s: %s -> %s' % (key, d, g))

                self.updateUser(google_user)
                count += 1

        return count

    # Reports
    def displayPerson(self, p, status):
        """Display a single person."""
        if status == 'due':
            print('   * '+str(p['full_name'])+' ['+str(p['person_type_name'])+'] is due on '+str(p['date_due'])[:10])
        elif status == 'overdue':
            print('   * '+str(p['full_name'])+' ['+str(p['person_type_name'])+'] was due on '+str(p['date_due'])[:10])
        else:
            print('Unknown status for '+p['full_name']+'!')

        if p['nocoi'] == '1':
            print('      * Locked for incomplete Disclosure')

        if p['nohst'] == '1':
            print('      * Locked for incomplete Human Subjects Training')

        if p['nopass'] == '1':
            print('      * Locked for unchanged Password')

    # people who are due
    def dueReport(self):
        """Return a report of people who are due."""
        due_people = []

        for p in self.peopledb.find({
                'terminated': False,
                'future_hire': '0',
                'status': 'incomplete',
        }).sort('date_due', 1):
            if p['date_due'] >= datetime.datetime.today():
                due_people.append(p)

        if due_people:
            print('Disclosures due in the next 30 days ('+str(len(due_people))+'):')

            display_date = ''
            for p in due_people:
                date_due = str(p['date_due'].date())
                if date_due != display_date:
                    display_date = date_due
                    print('\n   '+display_date+':')

                self.displayPerson(p, 'due')

    # breakdown of months when people are due
    def dueDatesReport(self, people):
        """Return a report of months when people are due."""
        # get people from mongo
        people = self.peopledb.find({
            'terminated': False,
            'future_hire': '0',
            'status': {'$ne': 'exempt'}
        }).sort([('first_name', 1), ('last_name', 1)])

        due_dates = {}
        for p in people:
            date_due = str(p['date_due'])[:7]
            if date_due in due_dates:
                due_dates[date_due] += 1
            else:
                due_dates[date_due] = 1

        for i in sorted(due_dates):
            print(i+': '+str(due_dates[i]))

    # people who are overdue
    def overdueReport(self):
        """Return a report of people who are overdue."""
        overdue_employees = []
        overdue_people = []
        overdue_associates = []
        locked_accounts = []

        for p in self.peopledb.find({
                'terminated': False,
                'future_hire': '0',
                'status': 'incomplete',
        }).sort('full_name', 1):

            if '1' in [p['nocoi'], p['nohst'], p['nopass'], p['nologin']]:
                locked_accounts.append(p)

            elif p['date_due'] < datetime.datetime.today():
                if p['person_type_id'] in ['4']:
                    overdue_employees.append(p)
                if p['person_type_id'] in ['3', '6', '10', '16']:
                    overdue_associates.append(p)
                else:
                    overdue_people.append(p)

        if overdue_employees:
            print('Employees with overdue disclosures ('+str(len(overdue_employees))+'):\n')
            for p in overdue_employees:
                self.displayPerson(p, 'overdue')
            print

        if overdue_people:
            print('Other Broadies with overdue disclosures ('+str(len(overdue_people))+'):\n')
            for p in overdue_people:
                self.displayPerson(p, 'overdue')
            print

        if overdue_associates:
            print('Associate/Core/Institute Members with overdue disclosures ('+str(len(overdue_associates))+'):\n')
            for p in overdue_associates:
                self.displayPerson(p, 'overdue')
            print

        if locked_accounts:
            print('Locked accounts ('+str(len(locked_accounts))+'):\n')
            for p in locked_accounts:
                self.displayPerson(p, 'overdue')
            print

    # people with status needs_review
    def needsReviewReport(self):
        """Display a report of people who need review."""
        # people = {}
        count = 0
        for p in self.peopledb.find({'status': 'needs_review', 'terminated': False}).sort('full_name', 1):
            print(p['full_name']+' <'+p['email']+'> "'+p['title']+'" http://broad.io/dr/'+str(p['pid']))
            count += 1
        print('TOTAL: '+str(count))

    def statsReport(self, people):
        """Return a report of stats."""
        disclosures = 0
        nodisclosures = 0

        undisclosed = {}
        peopleWithDisclosures = {}

        equity = 0
        govnonprofit = 0
        inventions = 0
        otheroutside = 0
        ownership = 0
        positions = 0
        remunerative = 0

        # for d in db.response.find( { 'active': True,
        #     'equity': { '$ne': '1' } ,
        #     'govnonprofit': { '$ne': '1' } ,
        #     'inventions': { '$ne': '1' } ,
        #     'otheroutside': { '$ne': '1' },
        #     'ownership': { '$ne': '1' } ,
        #     'positions': { '$ne': '1' } ,
        #     'remunerative': { '$ne': '1' } ,
        # } ):

        for d in self.responsedb.find({'active': True}):

            pid = int(d['pid'])
            if pid in people:
                p = people[pid]
                disclosed = False
                # skip terminated people
                if p['terminated']:
                    continue

                if 'equity' in d and str(d['equity']) == '1':
                    equity += 1
                    disclosed = True
                # if 'govnonprofit' in d and str(d['govnonprofit']) == '1':
                #     govnonprofit+=1
                #     disclosed=True
                if 'inventions' in d and str(d['inventions']) == '1':
                    inventions += 1
                    disclosed = True
                if 'otheroutside' in d and str(d['otheroutside']) == '1':
                    otheroutside += 1
                    disclosed = True
                if 'ownership' in d and str(d['ownership']) == '1':
                    ownership += 1
                    disclosed = True
                if 'positions' in d and str(d['positions']) == '1':
                    positions += 1
                    disclosed = True
                if 'remunerative' in d and str(d['remunerative']) == '1':
                    remunerative += 1
                    disclosed = True

                if disclosed:
                    disclosures += 1
                    peopleWithDisclosures[pid] = p
                else:
                    nodisclosures += 1
                    undisclosed[pid] = p

        print('People with disclosures: '+str(disclosures))
        print('   * equity: '+str(equity))
        print('   * govnonprofit: '+str(govnonprofit))
        print('   * inventions: '+str(inventions))
        print('   * otheroutside: '+str(otheroutside))
        print('   * ownership: '+str(ownership))
        print('   * positions: '+str(positions))
        print('   * remunerative: '+str(remunerative))

        print('People with no disclosures: '+str(nodisclosures))

        print('Total active Broadies who have submitted forms: '+str(disclosures+nodisclosures))

        # print('No Disclosures:')
        # for pid in sorted(undisclosed, key=lambda x: people[x]['full_name']):
        #     p = people[pid]
        #     print('   * '+p['full_name']+' https://disclosure.broadinstitute.org/admin/responses/'+str(pid))

        print('People who have disclosed something (except govnonprofit):')
        for pid in sorted(peopleWithDisclosures, key=lambda x: people[x]['full_name']):
            p = people[pid]
            print('   * '+p['full_name']+' https://disclosure.broadinstitute.org/admin/responses/'+str(pid))

    def summaryReport(self, people):
        """Display a summary report."""
        email_templates = self.getEmailTemplates()
        print('\nEmail Templates ('+str(len(email_templates))+'):')
        for eid in email_templates:
            e = email_templates[eid]
            type = e['param1']
            if type == 'soon':
                print('\n   Upcoming Due Date Email')
            elif type == 'overdue':
                print('\n   Overdue Email')
            print('   Subject: '+e['subject']+'\n      -----\n      '+e['body'].replace('\n', '\n      ')+'\n      -----')

        keywords = self.getKeywords()
        print('\nKeywords ('+str(len(keywords))+'):\n')
        for kid in keywords:
            k = keywords[kid]
            print('   * '+k['name'])

        people = self.getPeople()
        print('\nPeople ('+str(len(people))+'):')

        print('\n   Organization Report:')
        orgunits = {'none': 0}
        for p in self.peopledb.find({'status': 'incomplete', 'terminated': False}):
            if p['org_unit']:
                orgunit = p['org_unit'].split(' > ')
                if len(orgunit) > 1:
                    o = orgunit[0]+' > '+orgunit[1]
                else:
                    o = orgunit[0]
            else:
                o = None

            if not o:
                orgunits['none'] += 1
            elif o in orgunits:
                orgunits[o] += 1
            else:
                orgunits[o] = 1

        for o in sorted(orgunits):
            if o and orgunits[o]:
                print("{:>6}".format(orgunits[o])+' '+o)

        print('\n   Status Report:')
        status = {'none': 0, 'future': 0}

        for p in self.peopledb.find({'terminated': False}):
            # check if terminated
            if 'terminated' in p and p['terminated'] is True:
                status['terminated'] += 1

            # check if future_hire
            elif 'future_hire' in p and p['future_hire'] == '1':
                status['future'] += 1

            # check if no status
            elif 'status' not in p or not p['status']:
                status['none'] += 1

            # otherwise increment the count of the status of this person
            else:
                s = p['status']
                if s in status:
                    status[s] += 1
                else:
                    status[s] = 1

        for s in sorted(status):
            print('   * '+s+': '+str(status[s])+' people')

        print('\n   Incomplete Report:')
        person_type = {'none': 0, 'future': 0, 'terminated': 0, 'complete': 0, 'unknown': 0}

        for p in self.peopledb.find({'status': 'incomplete', 'terminated': False, 'future_hire': '0'}):
            # check if terminated
            if 'terminated' in p and p['terminated'] is True:
                person_type['terminated'] += 1

            # check if no status
            elif 'status' not in p or not p['status']:
                person_type['none'] += 1

            # check if status is incomplete
            elif p['status'] != 'incomplete':
                person_type['complete'] += 1

            # check if future_hire
            elif 'future_hire' in p and p['future_hire'] == '1':
                person_type['future'] += 1

            # otherwise make sure they have a person_type_id
            elif 'person_type_id' in p and p['person_type_id']:
                t = p['person_type_id']
                if t in person_type:
                    person_type[t] += 1
                else:
                    person_type[t] = 1

            # no person_type_id
            else:
                person_type['unknown'] += 1

        total = 0

        # types_by_name = {}
        # for tid in types:
        #     name = types[tid]['name']
        #     types_by_name[name] = tid

        # for type_name in sorted(types_by_name):
        #     tid = types_by_name[type_name]
        #     if tid in person_type:
        #         count = person_type[tid]
        #         total += count
        #         print('   * '+type_name+' ('+str(count)+')')
        #         del person_type[tid]

        print('   Total incomplete: '+str(total))

        users = self.getUsers()
        print('\nUsers ('+str(len(users))+'):')
        print('\n   Users with a Role:')
        for u in self.usersdb.find().sort('name'):
            if 'role' in u:
                print('   * '+u['name']+' <'+u['email']+'>: '+u['role'])

        # find terminated and future broadies
        todelete = []
        for pid in people:
            b = people[pid]
            if 'future_hire' in b and b['future_hire'] == '1':
                todelete.append(pid)
            elif 'terminated' in b and b['terminated']:
                todelete.append(pid)
        for pid in todelete:
            del people[pid]

        broademails = []
        for pid in people:
            b = people[pid]
            if 'username' in b and b['username']:
                broademails.append(b['username']+'@broadinstitute.org')

        active = len(broademails)

        users = self.usersdb.find()
        for u in users:
            e = u['email']
            if e in broademails:
                broademails.remove(e)

        broadlogins = [active, len(broademails)]

        print('\n   Active Broadies: '+str(broadlogins[0]))
        print('   Active Broadies who have logged in: '+str(broadlogins[0]-broadlogins[1]))
        print('   Active Broadies who have never logged in: '+str(broadlogins[1]))

        print('\nOther MongoDB Collections:')
        print('\n   '+'\n   '.join(self.getCollectionsReport()))

        print('\nNag report:')
        nags = 0
        for p in self.peopledb.find().sort('full_name'):
            if 'nag' in p:
                # print(p['full_name']+' '+str(p['nag']))
                nags += 1
        print('   * Nags sent: '+str(nags))

        print('\nOverdue report:')
        output = []
        for p in self.peopledb.find().sort('date_due'):
            if not p['terminated'] and str(p['date_due']) < time.strftime('%Y-%m-%d'):
                # tid = p['person_type_id']
                type = 'UNKNOWN'
                # if tid and tid in types:
                #     type = types[tid]['name']
                t = str(p['date_due'])+' '+p['first_name']+' '+p['last_name']+' ('+p['username']+') ['+type+'] http://broad.io/pv/'+str(p['pid'])
                output.append(t)
        for o in sorted(output):
            print('   * '+o)
        print('   Total overdue: '+str(len(output)))

        print('\nPeople with bad or missing due dates:')
        for p in self.peopledb.find().sort('start_date'):
            startdue = datetime.datetime.strptime(p['start_date'], '%Y-%m-%d') + datetime.timedelta(days=14)
            if 'date_due' in p and p['date_due'] < startdue:
                print('   * '+p['username']+' '+p['first_name']+' '+p['last_name']+' '+p['start_date']+' '+str(p['date_due'])+' has a bad due date')
                print('      * https://disclosure.broadinstitute.org/admin/responses/'+p['pid'])
                print('      * '+str(startdue))
            elif 'date_due' not in p:
                print('   * '+p['username']+' '+p['first_name']+' '+p['last_name']+' '+p['start_date']+' has a missing due date')
                print('      * https://disclosure.broadinstitute.org/admin/responses/'+p['pid'])
                print('      * '+str(startdue))

    def nagReport(self):
        """Display a report of users to nag."""
        print("Disclosure Nag Emails to Send:\n")
        # count = 0
        for p in self.peopledb.find({
                'terminated': False,
                'future_hire': '0',
                'status': 'incomplete',
                # 'person_type_id': '4',
        }).sort([('first_name', 1), ('last_name', 1)]):
            s = self.peopledb.find_one({
                'pid': p['supervisor_id'],
            })
            output = p['first_name']+' '+p['last_name']+' <'+p['email']+'>'
            if s:
                output += ' --> Supervisor: '+str(s['first_name'])+' '+str(s['last_name'])+' <'+s['email']+'>'
            print(output)

    # supervisors who have people that are due or overdue
    def supervisorReport(self, people):
        """Display a supervisor report of people that are due or overdue."""
        supervisors = {}
        for p in self.peopledb.find({
                'terminated': False,
                'future_hire': '0',
                'status': 'incomplete',
        }).sort('date_due', 1):
            if p['date_due'] < datetime.datetime.today():
                if p['person_type_id'] in ['3', '6', '10', '16']:
                    continue
                else:
                    sid = int(p['supervisor_id'])
                    if sid in supervisors:
                        supervisors[sid].append(p)
                    else:
                        supervisors[sid] = [p]
        if supervisors:
            print('Disclosure supervisor overdue report:')
            for sid in sorted(supervisors, key=lambda x: len(supervisors[x]), reverse=True):
                if sid:
                    s = people[sid]
                    print('\n'+s['full_name']+' <'+s['email']+'> ('+str(len(supervisors[sid]))+'):')
                    for p in supervisors[sid]:
                        self.displayPerson(p, 'overdue')

        if None in supervisors:
            print('\nNO SUPERVISOR:')
            for p in supervisors[None]:
                self.displayPerson(p, 'overdue')
