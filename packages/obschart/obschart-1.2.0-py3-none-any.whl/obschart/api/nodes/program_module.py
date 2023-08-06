from ..node import Node

programModuleFragment = """
fragment ProgramModule on ProgramModule {
    id
    name
    createdAt
}
"""


class ProgramModule(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def name(self):
        return self._data["name"]

    # def add_step(self, step_name: str, text_block_content: str):
    #     query = gql('''
    #         query ProgramModuleAddStepQuery($id: ID) {
    #             programModule(id: $id) {
    #                 data
    #             }
    #         }
    #     ''')

    #     variables = {}
    #     variables['id'] = self.id
    #     response = self._context.client._execute(query, variables)

    #     program_module_data = response['programModule']['data']

    #     new_block = {
    #         'type': 'text',
    #         'content': text_block_content
    #     }
    #     new_blocks = [new_block]
    #     new_action = {
    #         'type': 'blocks',
    #         'blocks': new_blocks
    #     }
    #     new_step = {
    #         'name': step_name,
    #         'action': new_action
    #     }
    #     program_module_data['action']['steps'].append(new_step)

    #     query = gql('''
    #         mutation ProgramModuleAddStepMutation($input: UpdateProgramModuleInput!)  {
    #             updateProgramModule(input: $input) {
    #                 programModule {
    #                     id
    #                 }
    #             }
    #         }
    #     ''')

    #     variables = {}
    #     variables['input'] = {}
    #     variables['input']['id'] = self.id
    #     variables['input']['data'] = program_module_data
    #     self._context.client._execute(query, variables)
