"""Tests for ord_schema.message_helpers."""

from absl.testing import absltest

from ord_schema import units
from ord_schema import message_helpers
from ord_schema.proto import reaction_pb2
from ord_schema.visualization import generate_text


class GenerateTextTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self._resolver = units.UnitResolver()

        reaction = reaction_pb2.Reaction()
        reaction.setup.is_automated = True
        reaction.inputs['dummy_input'].components.add().CopyFrom(
            message_helpers.build_compound(
                name='n-hexane',
                smiles='CCCCCC',
                role='reactant',
                amount='1 milliliters',
            )
        )
        reaction.inputs['dummy_input'].components.add().CopyFrom(
            message_helpers.build_compound(
                name='C1OCCC1',
                smiles='THF',
                role='solvent',
                amount='40 liters',
            )
        )
        reaction.conditions.pressure.atmosphere = (
            reaction_pb2.PressureConditions.Atmosphere.OXYGEN)
        reaction.conditions.stirring.rpm = 100
        reaction.conditions.temperature.type = (
            reaction_pb2.TemperatureConditions.TemperatureControl.OIL_BATH)
        reaction.conditions.temperature.setpoint.CopyFrom(
            reaction_pb2.Temperature(value=100,
                                     units=reaction_pb2.Temperature.CELSIUS))
        outcome = reaction.outcomes.add()
        outcome.reaction_time.CopyFrom(self._resolver.resolve('40 minutes'))
        outcome.products.add().compound.CopyFrom(
            message_helpers.build_compound(
                name='hexanone',
                smiles='CCCCC(=O)C',
                role='product',
            )
        )
        reaction.provenance.record_id = 'dummy_record_id'
        self._reaction = reaction

    def test_text(self):
        text = generate_text.generate_text(self._reaction)
        self.assertRegex(text, 'vessel')
        self.assertRegex(text, 'oil bath')
        self.assertRegex(text, 'after 40 min')
        self.assertRegex(text, 'hexanone')
        self.assertRegex(text, 'automatically')
        self.assertRegex(text, 'mL')

    def test_html(self):
        html = generate_text.generate_html(self._reaction)
        self.assertRegex(html, '<table')
        self.assertRegex(html, 'hexanone')
        self.assertRegex(html, 'under oxygen')
        self.assertRegex(html, '100 rpm')
        self.assertRegex(html, '40 min')
        self.assertRegex(html, 'as a solvent')
        self.assertRegex(html, '100 C')
        self.assertRegex(html, 'dummy_record_id')


if __name__ == '__main__':
    absltest.main()
