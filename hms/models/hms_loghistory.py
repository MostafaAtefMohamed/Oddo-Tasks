from odoo import fields,models

class HmsLoghistory(models.Model):
    _name = 'hms.loghistory'

    date=fields.Datetime()
    description=fields.Text()
    patient_id=fields.Many2one('hms.patient')
