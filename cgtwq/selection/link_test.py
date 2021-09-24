from cgtwq import _test, Field


def _use_shots_and_assets():
    db = _test.database()
    shots = db.module("shot", "info").filter(
        Field("shot.entity") == "SDKTEST_EP01_01_sc001",
    )
    assets = db.module("asset", "info").filter(
        Field("asset.entity") == "asset1",
    )
    assert assets and shots
    return shots, assets


@_test.skip_if_not_logged_in
def test_add():
    shots, assets = _use_shots_and_assets()

    shots.link.link(*assets)
    links = shots.link.get()
    assert all(i in links for i in assets)


@_test.skip_if_not_logged_in
def test_remove():
    shots, assets = _use_shots_and_assets()

    shots.link.remove(*assets)
    links = shots.link.get()
    assert not any(i in links for i in assets)
