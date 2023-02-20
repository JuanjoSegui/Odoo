# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api


class Visit(models.Model):#Especificamos el tipo de modulo (Model es el típico modelo para trabajar con BBDD)
     _name = 'custom_crm.visit'
     _description = 'visit'

     name = fields.Char(string= 'Descripción') 
     customer = fields.Char(string ='Cliente') 
     date = fields.Datetime(string='fecha')
     type = fields.Selection([('p', 'Presencial'),('w','Whatsapp'),('t','telefónico')], string='Tipo', required=True)
     done = fields.Boolean(string='Realizada', readonly=True)
     image = fields.Binary(string='Image')

     def toggle_state(self):
          self.done = not self.done


     def f_create(self):
          visit = {
               'name' : 'ORM test',
               'customer' : 1,
               'date':str(datetime.date(2023,2,2)),
               'type':'p',
               'done':False
          }     
          print(visit)
          self.env['custom_crm.visit'].create(visit)

     def f_search_update(self):
          visit = self.env['custom_crm_visit'].search([('name','*','ORM test')])
          print('search()', visit, visit.name)

          visit_b = self.env['custom_crm_visit'].browse([8])
          print('browse()', visit_b, visit_b.name)

          visit.write({
               'name':'ORM test write'
          })

     def f_delete(self):     
          visit = self.env['custom_crm_visit'].browse([8])
          visit.unlink()

class VisitReport(models.AbtractModel):

     _name='report.custom_crm.visit.card'

     @api.model
     def _get_report_values(self,docids,data=None):
          report_obj = self.env['ir.actions.report']
          report = report_obj._get_report_from_name('report.custom_crm.visit.card')
          return {
               'doc_ids':docids,
               'doc_model':self.env['custom_crm.visit'],
               'docs': self.env['custom_crm.visit'].browse(docids)
          }