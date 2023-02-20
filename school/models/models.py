# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import re
import secrets

_logger = logging.getLogger(__name__)


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string="Nombre",readonly=False,required=True,help="Introduce el Nombre")
    birth_year = fields.Integer()
    dni = fields.Char(string='DNI')
    password = fields.Char(default=lambda s: secrets.token_urlsafe(12))
    description = fields.Text()
    enrrollment_date = fields.Datetime(default=lambda self: fields.Datetime.now())
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200,max_heigth=200)
    #fields relacionaes 
    classroom = fields.Many2one('school.classroom',ondelete='set null', help='La clase a la que va')
    teachers = fields.Many2many('school.teacher',related='classroom.teachers', readonly=True)
    

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'

    name = fields.Char()
    students = fields.One2many(string='Students',comodel_name='school.student',inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teacher_classroom',
                                column1='classroom_id',
                                column2='teacher_id')
    teachers_ly = fields.Many2many(comodel_name='school.teacher_ly',
                                relation='teacher_classroom',
                                column1='classroom_id',
                                column2='teacher_id')   

    delegate = fields.Many2one('school.student',compute='_get_delegate')
    all_teachers = fields.Many2many('school.teacher',compute='_get_teachers')
    
    def _get_delegate(self):
        for c in self:
            c.delegate = c.students[0].id

    def _get_teachers(self):
        for c in self:
            c.all_teachers = c.teachers + c.teachers_ly


class teacher(models.Model):
    _name = 'chool.teacher'
    _description = 'Profesores'

    name = fields.Char()
    classroom = fields.Many2many(comodel_name='school.teacher',
                                relation='teacher_classroom',
                                column2='classroom_id',
                                column1='teacher_id')


#Para restringir solo Dni's validos, una expresion regular para insertar y un bucle for para recorer los dni introducidos
    @api.costrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z',re.I)
        for s in self:
            if regex.match(s.dni):
                _logger.info('El dni es correcto')
            else:
                raise ValidationError('El dni es incorrecto')


#Usamos la funcion propia de Postgree para que el DNI sea clave unica 
    _sql_constraints = [('dni_uniq','unique(dni)','El dni no puede repedirse')]

