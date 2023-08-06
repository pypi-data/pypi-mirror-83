
import numpy as np
import cogment_agent_toolbox.meta_data_pb2 as meta_data
import logging


class TensorGenerator:

    def __init__(self, actor_class):
        self._logger = logging.getLogger(__file__)
        self.default_repeated_count = 5

        self.actor_class = actor_class
        obs_tensor = self.compute_empty_tensor(self.actor_class.observation_space)
        self.state_size = self.compute_tensor_size(obs_tensor)

        action_tensor = self.compute_empty_tensor(self.actor_class.action_space)
        self.action_size = self.compute_tensor_size(action_tensor)

        # Action can be treated as a classification problem
        self.possible_actions = self.compute_classification_actions(action_tensor)

    def get_state_size(self):
        return self.state_size

    def get_action_size(self):
        return self.action_size

    def compute_tensor_size(self, actions_tensor):
        default_tensor_size = 0

        for action in actions_tensor:
            # Handle enum
            if action[0] == str:
                enum_size = action[2]
                default_tensor_size += enum_size
            else:
                default_tensor_size += 1

        return default_tensor_size


    def compute_empty_tensor(self, object_type):
        vector = []
        for descriptor in object_type.DESCRIPTOR.fields:
            options = descriptor.GetOptions()
            if (options.Extensions[meta_data.exclude_from_tensor] and options.Extensions[meta_data.exclude_from_tensor] is True):
                continue
            instance = object_type()
            value = getattr(instance, descriptor.name)
            value_type = type(value)
            if descriptor.type == descriptor.TYPE_MESSAGE:
                if descriptor.label == descriptor.LABEL_REPEATED:
                    repeated_count_hint = self.default_repeated_count
                    if options.Extensions[meta_data.repeated_count_hint]:
                        repeated_count_hint = options.Extensions[meta_data.repeated_count_hint]
                    list_instance = value.add()
                    list_type = type(list_instance)
                    out_map = map(self.compute_empty_tensor, [
                                  list_type for _ in range(repeated_count_hint)])
                    for element in list(out_map):
                        vector.extend(element)
                else:
                    vector.extend(self.compute_empty_tensor(value_type))
            elif descriptor.type == descriptor.TYPE_ENUM:
                enum_count = len(descriptor.enum_type.values)
                vector.append((str, options, enum_count))

            elif (descriptor.type == descriptor.TYPE_DOUBLE or
                    descriptor.type == descriptor.TYPE_FLOAT or
                    descriptor.type == descriptor.TYPE_INT32 or
                    descriptor.type == descriptor.TYPE_INT64 or
                    descriptor.type == descriptor.TYPE_BOOL):

                vector.append((value_type, options))
            elif descriptor.type == descriptor.TYPE_STRING:
                pass
            else:
                self._logger.warning(
                    f"Unknown {descriptor.full_name} : {value_type}")

        return vector

    def compute_tensor(self, obs):
        vector = []
        for descriptor in obs.DESCRIPTOR.fields:
            options = descriptor.GetOptions()
            if (options.Extensions[meta_data.exclude_from_tensor] and options.Extensions[meta_data.exclude_from_tensor] is True):
                continue
            value = getattr(obs, descriptor.name)
            if descriptor.type == descriptor.TYPE_MESSAGE:
                if descriptor.label == descriptor.LABEL_REPEATED:
                    repeated_count_hint = self.default_repeated_count
                    if options.Extensions[meta_data.repeated_count_hint]:
                        repeated_count_hint = options.Extensions[meta_data.repeated_count_hint]

                    while len(value) > repeated_count_hint:
                        value.pop()
                    while len(value) < repeated_count_hint:
                        value.add()

                    assert len(value) == repeated_count_hint

                    x = map(self.compute_tensor, value)
                    for l in list(x):
                        vector.extend(l)
                else:
                    vector.extend(self.compute_tensor(value))
            elif descriptor.type == descriptor.TYPE_ENUM:

                enum_count = len(descriptor.enum_type.values)

                for index in range(enum_count):
                    if value == descriptor.enum_type.values[index].number:
                        vector.append(1.0)
                    else:
                        vector.append(0.0)

            elif (descriptor.type == descriptor.TYPE_DOUBLE or
                    descriptor.type == descriptor.TYPE_FLOAT or
                    descriptor.type == descriptor.TYPE_INT32 or
                    descriptor.type == descriptor.TYPE_INT64):
                vector.append(value)
            elif descriptor.type == descriptor.TYPE_BOOL:
                if value is True:
                    vector.append(1.0)
                else:
                    vector.append(0.0)
            elif descriptor.type == descriptor.TYPE_STRING:
                pass
            else:
                self._logger.warning(
                    f"Unknown {descriptor.full_name} : {value}")

        return vector

    def __compute_action_from_tensor(self, action, vector_action):
        for descriptor in action.DESCRIPTOR.fields:
            value = getattr(action, descriptor.name)
            if descriptor.type == descriptor.TYPE_MESSAGE:
                if descriptor.label == descriptor.LABEL_REPEATED:
                    repeated_count_hint = self.default_repeated_count
                    if options.Extensions[meta_data.repeated_count_hint]:
                        repeated_count_hint = options.Extensions[meta_data.repeated_count_hint]
                    while len(value) > repeated_count_hint:
                        value.pop()
                    while len(value) < repeated_count_hint:
                        value.add()

                    assert len(value) == repeated_count_hint

                    map(self.__compute_action_from_tensor, value, vector_action)
                else:
                    self.__compute_action_from_tensor(value, vector_action)
            elif descriptor.type == descriptor.TYPE_ENUM:

                enum_count = len(descriptor.enum_type.values)
                max_index = 0
                max_value = float('-inf')
                for index in range(enum_count):
                    if vector_action[index] > max_value:
                        max_value = vector_action[index]
                        max_index = index

                enum_value = descriptor.enum_type.values[max_index].number
                setattr(action, descriptor.name, enum_value)

                for index in range(enum_count):
                    del vector_action[0]

            elif (descriptor.type == descriptor.TYPE_DOUBLE or
                    descriptor.type == descriptor.TYPE_FLOAT or
                    descriptor.type == descriptor.TYPE_INT32 or
                    descriptor.type == descriptor.TYPE_INT64):
                setattr(action, descriptor.name, vector_action[0])
                del vector_action[0]

            elif descriptor.type == descriptor.TYPE_BOOL:
                if vector_action[0] > 0.5:
                    setattr(action, descriptor.name, True)
                else:
                    setattr(action, descriptor.name, False)
                del vector_action[0]
            else:
                self._logger.warning(
                    f"Unknown {descriptor.full_name} : {value}")

    def compute_action_from_tensor(self, vector_action):
        action = self.actor_class.action_space()
        self.__compute_action_from_tensor(action, vector_action)
        return action

    # Classification problems utils

    def get_possible_actions(self):
        return self.possible_actions

    def get_classification_size(self):
        return len(self.possible_actions)

    def compute_classification_actions(self, actions_tensor):
        #  create an hot encoded version of our actions
        #  4 possible actions right, forward, rotate, shoot

        action_product = []
        two = [0.0, 1.0]
        enum_data = []

        for action in actions_tensor:
            min_value = -1.0
            max_value = 1.0
            increment = 1.0

            if action[1].Extensions[meta_data.min]:
                min_value = action[1].Extensions[meta_data.min]
            if action[1].Extensions[meta_data.max]:
                max_value = action[1].Extensions[meta_data.max]
            if action[1].Extensions[meta_data.increment]:
                increment = action[1].Extensions[meta_data.increment]

            values = [i for i in np.arange(min_value, max_value, increment)]
            values.append(max_value)

            # Handle enum
            if action[0] == str:
                enum_size = action[2]
                enum_data.append((len(action_product), enum_size))
                enum_inplace = list(range(enum_size))
                action_product.append(enum_inplace)

            elif action[0] == bool:
                action_product.append(two)
            else:
                action_product.append(values)

        list_without_enum = np.array(np.meshgrid(
            *action_product)).T.reshape(-1, len(action_product))

        final_list = list_without_enum

        if len(enum_data) > 0:
            final_list = []
            for index, enum_size in enum_data:
                identity = np.identity(enum_size)
                for idx, element in enumerate(list_without_enum):
                    element_list = element.tolist()
                    element_list[index:index+1] = identity[idx % enum_size]
                    final_list.append(element_list)
            final_list = np.array(final_list)

        return final_list

    def compute_choice_from_action(self, action_tensor):
        min_dot_diff = 50
        selected_choice = 0

        for choice, poss in enumerate(self.possible_actions):
            diff = action_tensor - poss
            dot_diff = np.dot(diff, diff)

            if dot_diff < min_dot_diff:
                selected_choice = choice
                min_dot_diff = dot_diff
        return selected_choice

    def convert_choice_in_action(self, choice):
        action_tensor = self.possible_actions[choice].tolist()
        action = self.compute_action_from_tensor(action_tensor)
        return action
