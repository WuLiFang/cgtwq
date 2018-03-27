# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from .base import BaseSelection


class MessageMixin(BaseSelection):
    """Send message with the selection.  """

    def send_message(self, title, content, *to, **kwargs):
        """Send message to users.

        Args:
            title (text_type): Message title.
            content (text_type): Message content, support html.
            *to: Users that will recives message, use account_id.
            **kwargs:
                from_: Unknown effect. used in `cgtw` module.
        """
        # pylint: disable=invalid-name

        from_ = kwargs.get('from_')

        return self.call(
            'c_msg', 'send_task',
            task_id=self[0],
            account_id_array=to,
            title=title,
            content=content,
            from_account_id=from_
        )
