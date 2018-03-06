# coding: utf-8
from ticket.models import Ticket


class TicketSql:
    @staticmethod
    def get_ticket(ticket):
        return Ticket.objects.filter(ticket=ticket)

    @staticmethod
    def create_ticket(**kwargs):
        Ticket.objects.create(**kwargs)

    @staticmethod
    def delete_ticket(ticket):
        Ticket.objects.filter(ticket=ticket).delete()

ticket_sql = TicketSql()
