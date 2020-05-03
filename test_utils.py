import unittest

from utils import labels_diff, labels_sync


class UtilsTestCase(unittest.TestCase):
    def test_labels_diff(self):
        result = labels_diff(
            {
                "current": [
                    {
                        "color": "#428BCA",
                        "created_at": "2020-05-03 10:43:50 UTC",
                        "description": None,
                        "group_id": None,
                        "id": 14829548,
                        "project_id": 18530689,
                        "template": False,
                        "title": "workflow::doing",
                        "type": "ProjectLabel",
                        "updated_at": "2020-05-03 10:43:50 UTC",
                    },
                    {
                        "color": "#428BCA",
                        "created_at": "2020-05-03 10:43:50 UTC",
                        "description": None,
                        "group_id": None,
                        "id": 14829548,
                        "project_id": 18530689,
                        "template": False,
                        "title": "label2",
                        "type": "ProjectLabel",
                        "updated_at": "2020-05-03 10:43:50 UTC",
                    },
                ],
                "previous": [
                    {
                        "color": "#0033CC",
                        "created_at": "2020-05-01 23:03:43 UTC",
                        "description": None,
                        "group_id": None,
                        "id": 14820514,
                        "project_id": 18530689,
                        "template": False,
                        "title": "label1",
                        "type": "ProjectLabel",
                        "updated_at": "2020-05-01 23:03:43 UTC",
                    },
                    {
                        "color": "#428BCA",
                        "created_at": "2020-05-03 10:43:50 UTC",
                        "description": None,
                        "group_id": None,
                        "id": 14829548,
                        "project_id": 18530689,
                        "template": False,
                        "title": "workflow::doing",
                        "type": "ProjectLabel",
                        "updated_at": "2020-05-03 10:43:50 " "UTC",
                    },
                ],
            }
        )
        self.assertIn("label1", result["label_removed"])
        self.assertIn("label2", result["label_added"])

    def test_sync_labels(self):
        def sync_filter(label):
            return label.startswith("workflow::") or label in ["label2"]

        self.assertEqual(
            labels_sync(
                source=set(["label1", "workflow::ready-for-merge"]),
                destination=set(["label3", "label2", "workflow::doing"]),
                sync_filter=sync_filter,
            ),
            set(["label3", "workflow::ready-for-merge"]),
        )


if __name__ == "__main__":
    unittest.main()
