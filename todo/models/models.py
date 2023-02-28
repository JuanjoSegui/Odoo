# -*- coding: utf-8 -*-

from odoo import models, fields, api


class todo(models.Model):
    _name = 'td.todo'
    _description = 'td.todo'

    name = fields.Char('Nombre')
    status = fields.selection(selection=[('borrador':'borrador'), ('hecho':'hecho')])
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
