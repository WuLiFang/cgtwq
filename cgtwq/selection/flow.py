# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .base import SelectionAttachment


class SelectionFlow(SelectionAttachment):
    """Flow operation on selection.  """

    def approve(self, field, message=''):
        node_data = self._get_action_qc_data(field, 'Approve')
        self._update_flow(node_data, message)

    def retake(self, field, message=''):
        node_data = self._get_action_qc_data(field, 'Retake')
        self._update_flow(node_data, message)

    def close(self, field, message=''):
        node_data = self._get_action_qc_data(field, 'Close')
        self._update_flow(node_data, message)

    def _pipeline(self):
        name = self.select['pipeline'][0]
        return next(i for i in self.select.module.pipelines() if i.name == name)

    def _get_field_id(self, field):
        field = self.select.module.field(field)
        return next(i.id for i in self.select.module.fields() if i.sign == field)

    def _neighbor_flow(self, pipeline_id):
        flow = self.select.module.flow()
        curr_ = next(i for i in flow if i.pipeline_id == pipeline_id)
        index = flow.index(curr_)
        prev_ = flow[index - 1] if index-1 >= 0 else None
        next_ = flow[index + 1] if index+1 < len(flow) else None
        return prev_, curr_, next_

    def _get_action_qc_data(self, field, action):
        return next(i[0] for i in self._get_qc_data(field) if i[0]['name'] == action)

    def _get_qc_data(self, field):
        assert self.select.module.is_field_in_flow(field)
        assert self.has_field_permission(field)
        field = self.select.module.field(field)
        resp = self.call('c_work_flow', 'get_click_qc_data',
                         field_sign=field,
                         task_id_array=self.select)
        return resp.data

    def _update_flow(self, node_data, message):
        # pipeline = self._pipeline()
        # prev_flow, curr_flow, next_flow = self._neighbor_flow(pipeline.id)
        # node_data = {
        #     'set_field_id':  self._get_field_id(field),
        #     'flow_id': curr_flow.flow_id,
        #     'name': action,
        #     'previous_pipeline_id': prev_flow.pipeline_id if prev_flow else '',
        #     'next_pipeline_id': next_flow.pipeline_id if next_flow else '',
        #     'status_msg_to': '',
        #     'plugin_id': '',
        #     'type': action,
        # }
        node_data['previous_pipeline_id'] = ''
        resp = self.call('c_work_flow', 'update_flow',
                         node_data_array=node_data,
                         task_id_array=self.select,
                         text=message,)
        assert resp.data

    def has_field_permission(self, field):
        """Return if current user has permission to edit the field.  """

        field = self.select.module.field(field)
        resp = self.call(
            'c_work_flow', 'is_status_field_has_permission',
            field_sign=field,
            task_id_array=self.select
        )
        return resp.data
