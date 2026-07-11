from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notebook.models import Note

User = get_user_model()


class Command(BaseCommand):
    help = '指定ユーザーに復習確認用の過去ノートを作成する'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='対象ユーザーのメールアドレス')

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'ユーザーが見つかりません: {email}'))
            return

        targets = [
            (1, '昨日のノート'),
            (7, '1週間前のノート'),
            (14, '2週間前のノート'),
            (30, '1ヶ月前のノート'),
        ]

        for days, title in targets:
            target_date = date.today() - timedelta(days=days)
            if Note.objects.filter(user=user, date=target_date).exists():
                self.stdout.write(f'skip: {target_date} は既に存在')
                continue
            note = Note.objects.create(
                user=user, title=title, content=f'{title}の内容です。'
            )
            Note.objects.filter(id=note.id).update(date=target_date)
            self.stdout.write(self.style.SUCCESS(f'created: {target_date} ({title})'))