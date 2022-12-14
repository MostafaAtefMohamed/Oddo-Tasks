from odoo import models,fields,api
import re
from odoo.exceptions import ValidationError,UserError
from datetime import date


class Patient(models.Model):
    _name = 'hms.patient'
    first_name=fields.Char()
    last_name=fields.Char()
    email=fields.Char()
    birth_date=fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('O', 'O'), ('A+', 'A+')]
    )
    pcr = fields.Boolean()
    image=fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')
    login_time=fields.Datetime()
    department_ids=fields.Many2one('hms.departments')
    department_capacity=fields.Integer(related='department_ids.capacity')
    doctors=fields.Many2many('hms.doctor')
    state=fields.Selection(
        [('undetermined','Undetermined'),('good','Good'),('fair','Fair'),('serious','Serious') ]
        , default='undetermined'
    )
    hms_log=fields.One2many('hms.loghistory','patient_id')
    crm = fields.Many2many('res.partner')



    @api.constrains('email')
    def _check_email(self):
        count_email = self.search_count([('email', '=', self.email)])
        if count_email > 1 and self.email is not False:
            raise UserError('The email already registered, please use another email!')



    def action_undetermined(self):
        self.state = "undetermined"
        new_log = self.env["hms.loghistory"].create({"description": "The State now is Undetermined", "patient_id": self.id})
        self.env.cr.commit()

    def action_good(self):
        self.state = "good"
        new_log = self.env["hms.loghistory"].create({"description": "The State now is Good", "patient_id": self.id})
        self.env.cr.commit()

    def action_fair(self):
        self.state = "fair"
        new_log = self.env["hms.loghistory"].create({"description": "The State now is Fair", "patient_id": self.id})
        self.env.cr.commit()

    def action_serious(self):
        self.state = "serious"
        new_log = self.env["hms.loghistory"].create({"description": "The State now is Serious", "patient_id": self.id})
        self.env.cr.commit()





    @api.onchange('age')
    def _onchange_age(self):
        if self.age<30 and self.age!=0:
            self.pcr=True
            return {
                'warning': {
                    'title': 'message',
                    'message': 'the pcr have been checked because age less than 30'
                }
            }
        else:
            self.pcr=False


    @api.constrains("email")
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        for record in self:
            if not re.search(regex, record.email):
                raise ValidationError("invalid email please enter some thing like this = ahmed_ragab@gmail.com")

    @api.onchange('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = date.today().year - rec.birth_date.year
            else:
                rec.age = 0