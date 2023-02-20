# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Visit(models.Model):#Especificamos el tipo de modulo (Model es el típico modelo para trabajar con BBDD)
     _name = 'custom_crm.visit'
     _description = 'visit'

     name = fields.Char(string= 'Descripción') 
     customer = fields.Char(string ='Cliente') 
     date = fields.Datetime(string='fecha')
     type = fields.Selection([('p', 'Presencial'),('w','Whatsapp'),('t','telefónico')], string='Tipo', required=True)
     done = fields.Boolean(string='Realizada', readonly=True)
