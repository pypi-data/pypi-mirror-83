from sktmls.models.contrib import MbrSimilarBenefitModel


class TestMbrSimilarBenefitModel:
    def test_000_mbr_valid_1a(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["a3", "b2", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(
            [
                "1234567890",
                ["use_benefit1", "use_benefit2", "use_benefit3"],
                ["like_benefit1", "like_benefit2", "like_benefit3"],
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "a3"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

    def test_001_mbr_valid_1b(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["b2", "a3", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=1,
        )

        results = mbm.predict(
            [
                "1234567890",
                ["use_benefit1", "use_benefit2", "use_benefit3"],
                ["like_benefit1", "like_benefit2", "like_benefit3"],
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 1

        item = results["items"][0]
        assert item["id"] == "b2"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

    def test_002_mbr_valid_2(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["a3", "b2", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(
            [
                "1234567890",
                ["use_benefit1", "use_benefit2", "use_benefit3"],
                ["like_benefit1", "like_benefit2", "like_benefit3"],
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 2

        item = results["items"][0]
        assert item["id"] == "a3"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

        item = results["items"][1]
        assert item["id"] == "b2"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

    def test_003_mbr_valid_3(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["a3", "b2", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=3,
        )

        results = mbm.predict(
            [
                "1234567890",
                ["use_benefit1", "use_benefit2", "use_benefit3"],
                ["like_benefit1", "like_benefit2", "like_benefit3"],
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 2

        item = results["items"][0]
        assert item["id"] == "a3"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

        item = results["items"][1]
        assert item["id"] == "b2"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] in ["use_brand_test_brand", "like_brand_test_brand"]
        assert item["props"]["context_nm"] in ["브랜드_test_brand_사용_유사혜택", "브랜드_test_brand_좋아요_유사혜택"]

    def test_004_mbr_valid_only_use(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["a3", "b2", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(
            [
                "1234567890",
                ["use_benefit1", "use_benefit2", "use_benefit3"],
                None,
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 2

        item = results["items"][0]
        assert item["id"] == "a3"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "use_brand_test_brand"
        assert item["props"]["context_nm"] == "브랜드_test_brand_사용_유사혜택"

        item = results["items"][1]
        assert item["id"] == "b2"
        assert item["type"] == "test_type"
        assert item["props"]["context_id"] == "use_brand_test_brand"
        assert item["props"]["context_nm"] == "브랜드_test_brand_사용_유사혜택"

    def test_005_mbr_valid_all_none(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "brand": {
                    "brand_id": "test_brand",
                },
                "similar_items": ["a3", "b2", "c9"],
            },
        )

        mbm = MbrSimilarBenefitModel(
            model_name="test_model",
            model_version="test_version",
            features=[
                "user_id",
                "use_benefit",
                "like_benefit",
                "available_benefit_activity",
                "available_benefit_asianfood",
                "available_benefit_beauty",
            ],
            categories=["mbr_activity", "mbr_asianfood", "mbr_beauty"],
            item_type="test_type",
            num_pick=2,
        )

        results = mbm.predict(
            [
                "1234567890",
                None,
                None,
                ["a1", "a2", "a3", "a4"],
                None,
                ["b1", "b2", "3", "4"],
            ]
        )
        assert len(results["items"]) == 0
