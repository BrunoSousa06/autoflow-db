import unittest

from review_rds_plan import validate_plan


class ReviewRdsPlanTests(unittest.TestCase):
    def test_accepts_no_changes(self):
        self.assertEqual(validate_plan({"resource_changes": []}), 0)

    def test_accepts_non_destructive_changes(self):
        plan = {
            "resource_changes": [
                {"address": "aws_db_instance.autoflow_rds", "change": {"actions": ["update"]}},
                {"address": "aws_security_group.rds_sg", "change": {"actions": ["create"]}},
            ]
        }
        self.assertEqual(validate_plan(plan), 2)

    def test_rejects_destroy_of_any_resource(self):
        plan = {
            "resource_changes": [
                {"address": "aws_db_instance.autoflow_rds", "change": {"actions": ["delete"]}}
            ]
        }
        with self.assertRaisesRegex(ValueError, "exclusão/substituição"):
            validate_plan(plan)

    def test_rejects_replace_even_for_network_resources(self):
        plan = {
            "resource_changes": [
                {"address": "aws_subnet.private", "change": {"actions": ["delete", "create"]}}
            ]
        }
        with self.assertRaisesRegex(ValueError, "exclusão/substituição"):
            validate_plan(plan)

    def test_rejects_change_to_rds_identifier_or_backup_configuration(self):
        for attribute in (
            "identifier",
            "backup_retention_period",
            "skip_final_snapshot",
            "final_snapshot_identifier",
            "deletion_protection",
        ):
            with self.subTest(attribute=attribute):
                plan = {
                    "resource_changes": [
                        {
                            "address": "aws_db_instance.autoflow_rds",
                            "type": "aws_db_instance",
                            "change": {
                                "actions": ["update"],
                                "before": {attribute: "old"},
                                "after": {attribute: "new"},
                            },
                        }
                    ]
                }
                with self.assertRaisesRegex(ValueError, "exclusão/substituição"):
                    validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
