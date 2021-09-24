from cgtwq import _test, Field


@_test.skip_if_not_logged_in
def test_add():
    db = _test.database()
    shots = db.module("shot", "info").filter(
        Field("shot.entity") == "SDKTEST_EP01_01_sc001",
    )
    assets = db.module("asset", "info").filter(
        Field("asset.entity") == "asset1",
    )
    assert assets and shots

    shots.link.link(*assets)
    links = shots.link.get()
    assert all(i in links for i in assets)
