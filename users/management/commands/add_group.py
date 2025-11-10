from django.core.management import BaseCommand
from django.db.models import Q
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help="Create chosen group"

    def add_arguments(self, parser):
        parser.add_argument("group_name",type=str, help="Name of group" )

    def handle(self, *args, **options):
        group_name = options["group_name"]
        if group_name in ["Managers", "Users"]:

            if group_name == "Managers":
                group, created = Group.objects.get_or_create(name=group_name)
                permissions = Permission.objects.filter(Q(codename__startswith=("can_manage_")) |
                                                        Q(codename__in=["delete_mailing",
                                                                      "view_mailing",
                                                                      "delete_recipient",
                                                                      "view_recipient",])
                                                        )
                print(permissions)
                group.permissions.set(permissions)
                group.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Группе '{group_name}' назначено {permissions.count()} прав."
                ))

                if created:
                    self.stdout.write(self.style.NOTICE("Группа была создана, так как ранее не существовала."))

            if group_name == "Users":
                group, created = Group.objects.get_or_create(name=group_name)
                permissions = Permission.objects.filter(
                    Q(codename__startswith='add_') |
                    Q(codename__startswith='change_') |
                    Q(codename__startswith='delete_') |
                    Q(codename__startswith='view_') |
                    Q(codename__in=["add_mailing", "delete_mailing", "view_mailing", "change_mailing",
                                                                      "add_recipient", "delete_recipient", "view_recipient", "change_recipient",
                                                                      "add_letter", "delete_letter", "view_letter", "change_letter"])
                )
                permissions = Permission.objects.filter(codename__in=["add_mailing", "delete_mailing", "view_mailing", "change_mailing",
                                                                      "add_recipient", "delete_recipient", "view_recipient", "change_recipient",
                                                                      "add_letter", "delete_letter", "view_letter", "change_letter"])
                print(permissions)
                group.permissions.set(permissions)
                group.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Группе '{group_name}' назначено {permissions.count()} прав."
                ))

                if created:
                    self.stdout.write(self.style.NOTICE("Группа была создана, так как ранее не существовала."))

