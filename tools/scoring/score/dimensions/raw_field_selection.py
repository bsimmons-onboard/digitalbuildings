# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Core component """

from score.dimensions.dimension import Dimension
from score.constants import FileTypes

PROPOSED, SOLUTION = FileTypes


class RawFieldSelection(Dimension):
  """
  Quantifies whether the correct raw fields
  (e.g. "points.chilled_water_flowrate_sensor.present_value")
  were mapped (versus ignored) in the proposed file.
  """
  def evaluate(self):
    # Combine translations for all devices within the dictionary
    condense_translations = lambda file_type: [
        matched_translations[file_type]
        for matched_translations in self.translations.values()
        if matched_translations[file_type]
    ]

    solution_condensed = condense_translations(SOLUTION)
    proposed_condensed = condense_translations(PROPOSED)

    # Account for empty list
    solution_translations = solution_condensed and solution_condensed[0]
    proposed_translations = proposed_condensed and proposed_condensed[0]

    raw_field_names = lambda translations: set([
        translation.raw_field_name
        for standard_field_name, translation in translations
    ])

    solution_fields = raw_field_names(solution_translations)
    proposed_fields = raw_field_names(proposed_translations)

    correct_fields = proposed_fields.intersection(solution_fields)
    incorrect_fields = proposed_fields.difference(solution_fields)

    self.correct_reporting = len(correct_fields)
    self.correct_ceiling_reporting = len(set(solution_translations))
    self.incorrect_reporting = len(incorrect_fields)

    return self
