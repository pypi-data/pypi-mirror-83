from mongodb_migrations.base import BaseMigration

# -----------------------------------------------------------------------------------------------------------------
# -- Collections Update
# -----------------------------------------------------------------------------------------------------------------


class Migration(BaseMigration):
    def upgrade(self):
        self.db.mongodb_model.save({"id": "test_id", "title": "test", "year": 2020})

    def downgrade(self):
        self.db.mongodb_model.drop()
