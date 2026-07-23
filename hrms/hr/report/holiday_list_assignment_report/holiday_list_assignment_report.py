# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 150,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Holiday List"),
			"fieldname": "holiday_list",
			"fieldtype": "Link",
			"options": "Holiday List",
			"width": 200,
		},
		{
			"label": _("Assignment Starts From"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"width": 150,
		},
		{
			"label": _("Company"),
			"fieldname": "employee_company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 150,
		},
	]


def get_data(filters):
	HLA = frappe.qb.DocType("Holiday List Assignment")
	Employee = frappe.qb.DocType("Employee")

	query = (
		frappe.qb.from_(HLA)
		.inner_join(Employee)
		.on(HLA.assigned_to == Employee.name)
		.select(
			HLA.assigned_to.as_("employee"),
			Employee.employee_name,
			HLA.holiday_list,
			HLA.from_date,
			HLA.employee_company,
		)
		.where(HLA.applicable_for == "Employee")
		.where(HLA.docstatus != 2)
	)

	if filters:
		if filters.get("company"):
			query = query.where(HLA.employee_company == filters["company"])
		if filters.get("holiday_list"):
			query = query.where(HLA.holiday_list == filters["holiday_list"])
		if filters.get("employee"):
			query = query.where(HLA.assigned_to == filters["employee"])
		if filters.get("from_date"):
			query = query.where(HLA.from_date >= filters["from_date"])
		if filters.get("to_date"):
			query = query.where(HLA.from_date <= filters["to_date"])

	return query.run(as_dict=True)
