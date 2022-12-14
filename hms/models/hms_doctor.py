from odoo import fields,models

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'FirstName'

    FirstName=fields.Char()
    LastName=fields.Char()
    image=fields.Binary()