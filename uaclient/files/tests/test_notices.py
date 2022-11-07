import os

import mock
import pytest

from uaclient.conftest import FakeNotice
from uaclient.files import notices
from uaclient.files.notices import NoticeFileDetails, Notices


class TestNotices:
    @pytest.mark.parametrize(
        "label,content",
        (
            (
                NoticeFileDetails(
                    order_id="10",
                    label="test_file",
                    is_permanent=True,
                    message="test",
                ),
                "We are a test",
            ),
        ),
    )
    @mock.patch("uaclient.files.notices.system.write_file")
    def test_add(
        self,
        sys_write_file,
        label,
        content,
    ):
        notice = Notices()
        notice.add(True, label, content)
        assert [
            mock.call(os.path.join(notice.directory, "10-test_file"), content)
        ] == sys_write_file.call_args_list

    @pytest.mark.parametrize(
        "label,content",
        (
            (
                NoticeFileDetails(
                    order_id="10",
                    label="test_file",
                    is_permanent=True,
                    message="test",
                ),
                "We are a test",
            ),
        ),
    )
    def test_add_duplicate_label(
        self,
        label,
        content,
    ):
        notice = Notices()
        notice.add(True, label, content)
        with mock.patch(
            "uaclient.files.notices.system.write_file"
        ) as sys_write_file:
            notice.add(True, label, content)
            assert [] == sys_write_file.call_args_list

    @pytest.mark.parametrize(
        "label,content",
        (
            (
                NoticeFileDetails(
                    order_id="10",
                    label="test_file",
                    is_permanent=True,
                    message="test",
                ),
                "We are a test",
            ),
        ),
    )
    @mock.patch("uaclient.files.notices.system.remove_file")
    def test_remove(
        self,
        sys_remove_file,
        label,
        content,
    ):
        notice = Notices()
        notice.add(True, label, content)
        notice.remove(True, label)
        assert [
            mock.call(os.path.join(notice.directory, "10-test_file"))
        ] == sys_remove_file.call_args_list

    @pytest.mark.parametrize(
        "label,content",
        (
            (
                NoticeFileDetails(
                    order_id="10",
                    label="test_file",
                    is_permanent=True,
                    message="test",
                ),
                "We are a test",
            ),
        ),
    )
    @mock.patch("uaclient.files.notices.system.remove_file")
    def test_remove_non_present_label(
        self,
        sys_remove_file,
        label,
        content,
    ):
        notice = Notices()
        notice.add(True, label, content)
        diff_notice = NoticeFileDetails(
            order_id="10",
            label="test_file_test",
            is_permanent=True,
            message="test",
        )
        notice.remove(True, diff_notice)
        assert [] == sys_remove_file.call_args_list

    @mock.patch("uaclient.files.notices.Notices.read")
    @mock.patch("uaclient.files.notices.Notices.remove")
    @mock.patch("uaclient.files.notices.Notices.add")
    def test_notice_module(
        self, notice_cls_add, notice_cls_remove, notice_cls_read
    ):
        notices.add(True, FakeNotice.a)
        assert [
            mock.call(True, FakeNotice.a, "notice_a"),
        ] == notice_cls_add.call_args_list
        notices.remove(True, FakeNotice.a)
        assert [
            mock.call(True, FakeNotice.a)
        ] == notice_cls_remove.call_args_list
        notices.list()
        assert 1 == notice_cls_read.call_count
