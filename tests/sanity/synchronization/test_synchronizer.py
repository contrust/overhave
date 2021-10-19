from typing import List

import pytest

from demo.settings import OverhaveDemoAppLanguage
from overhave import db
from overhave.entities import FeatureTypeModel, SystemUserModel
from overhave.scenario.errors import FeatureNameParsingError
from overhave.synchronization import OverhaveSynchronizer
from overhave.synchronization.synchronizer import FeatureInfoUserNotFoundError


def _check_db_no_features() -> None:
    with db.create_session() as session:
        features = session.query(db.Feature).all()
        assert not features


@pytest.mark.usefixtures("database")
class TestOverhaveSynchronizer:
    """ Sanity tests for application admin mode. """

    @pytest.mark.parametrize("test_demo_language", [OverhaveDemoAppLanguage.RU], indirect=True)
    @pytest.mark.parametrize("create_db_features", [False])
    def test_synchronize_not_create_ru(
        self, test_resolved_synchronizer: OverhaveSynchronizer, create_db_features: bool
    ) -> None:
        test_resolved_synchronizer.synchronize(create_db_features=create_db_features)
        _check_db_no_features()

    @pytest.mark.parametrize("test_demo_language", [OverhaveDemoAppLanguage.EN], indirect=True)
    @pytest.mark.parametrize("create_db_features", [False])
    def test_synchronize_not_create_en(
        self, test_resolved_synchronizer: OverhaveSynchronizer, create_db_features: bool
    ) -> None:
        with pytest.raises(FeatureNameParsingError):
            test_resolved_synchronizer.synchronize(create_db_features=create_db_features)
        _check_db_no_features()

    @pytest.mark.parametrize("test_demo_language", [OverhaveDemoAppLanguage.RU], indirect=True)
    @pytest.mark.parametrize("create_db_features", [True])
    @pytest.mark.parametrize("test_system_user_login", ["alternate_user_login"], indirect=True)
    def test_synchronize_create_ru_without_user(
        self, test_resolved_synchronizer: OverhaveSynchronizer, test_db_user: SystemUserModel, create_db_features: bool
    ) -> None:
        with pytest.raises(FeatureInfoUserNotFoundError):
            test_resolved_synchronizer.synchronize(create_db_features=create_db_features)

    @pytest.mark.parametrize("test_demo_language", [OverhaveDemoAppLanguage.RU], indirect=True)
    @pytest.mark.parametrize("create_db_features", [True])
    @pytest.mark.parametrize("test_system_user_login", ["admin"], indirect=True)
    def test_synchronize_create_ru(
        self,
        test_resolved_synchronizer: OverhaveSynchronizer,
        test_db_user: SystemUserModel,
        test_db_feature_types: List[FeatureTypeModel],
        create_db_features: bool,
    ) -> None:
        test_resolved_synchronizer.synchronize(create_db_features=create_db_features)
