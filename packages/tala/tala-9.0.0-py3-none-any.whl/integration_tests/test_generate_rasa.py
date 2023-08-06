import pytest

from tala.nl.languages import SUPPORTED_RASA_LANGUAGES

from .expected_generate_rasa_output import EXPECTED_BOILERPLATE
from .console_script_mixin import ConsoleScriptTestMixin


class TestGenerateRASAIntegration(ConsoleScriptTestMixin):
    def setup(self):
        super(TestGenerateRASAIntegration, self).setup()

    @pytest.mark.parametrize("language", SUPPORTED_RASA_LANGUAGES)
    def test_that_generating_boilerplate_ddd_succeeds(self, language):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_ddd_folder():
            self._given_added_grammar(language)
        with self._given_changed_directory_to_target_dir():
            self._given_added_language(language)
        self._then_result_is_successful()

    def _when_generating(self, language="eng"):
        self._run_tala_with(["generate", "rasa", "test_ddd", language])

    @pytest.mark.parametrize("language", SUPPORTED_RASA_LANGUAGES)
    def test_stdout_when_generating_boilerplate_ddd(self, language):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_ddd_folder():
            self._given_added_grammar(language)
        with self._given_changed_directory_to_target_dir():
            self._given_added_language(language)
            self._when_running_command(f"tala generate rasa test_ddd {language}")
        self._then_stdout_matches(EXPECTED_BOILERPLATE[language])

    def test_stdout_when_generating_ddd_with_an_action(self):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_ddd_folder():
            self._given_ontology_contains("""
<ontology name="TestDddOntology">
  <action name="call"/>
</ontology>""")
            self._given_grammar_contains(
                """
<grammar>
  <action name="call">
    <verb-phrase>
      <verb ref="call"/>
    </verb-phrase>
  </action>
  <lexicon>
    <verb id="call">
      <infinitive>call</infinitive>
    </verb>
  </lexicon>
  <request action="call"><utterance>make a call</utterance></request>
</grammar>"""
            )
        with self._given_changed_directory_to_target_dir():
            self._given_ddd_verifies_successfully()
            self._when_running_command("tala generate rasa test_ddd eng")
        self._then_stdout_matches(
            r'''## intent:test_ddd:action::call
- make a call

## intent:NEGATIVE
- aboard
- about
''')  # yapf: disable  # noqa: W293

    def _given_ddd_verifies_successfully(self):
        self._run_tala_with(["verify"])

    def test_generating_for_unknown_ddd(self):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_target_dir():
            self._when_running_command("tala generate rasa unknown-ddd eng")
        self._then_stderr_matches("UnexpectedDDDException: Expected DDD 'unknown-ddd' to exist but it didn't")

    def test_generating_for_unknown_language(self):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_target_dir():
            self._when_running_command("tala generate rasa test_ddd unknown-language")
        self._then_stderr_matches("tala generate: error: argument language: invalid choice: 'unknown-language'")

    def test_generating_for_unsupported_language(self):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_target_dir():
            self._when_running_command("tala generate rasa test_ddd pes")
        self._then_stderr_matches(
            r"Expected one of the supported languages \['eng'\] in backend config "
            "'backend.config.json', but got 'pes'"
        )

    def test_stdout_when_generating_ddd_with_action_and_question_and_sortal_and_propositional_answers_without_rgl(self):
        self._given_created_ddd_in_a_target_dir()
        with self._given_changed_directory_to_ddd_folder():
            self._given_rgl_is_disabled()
            self._given_ontology_contains(
                """
<ontology name="TestDddOntology">
  <sort name="contact"/>
  <sort name="phone_number" dynamic="true"/>
  <predicate name="phone_number_of_contact" sort="phone_number"/>
  <predicate name="selected_contact" sort="contact"/>
  <individual name="contact_john" sort="contact"/>
  <action name="buy"/>
  <predicate name="selected_amount" sort="integer"/>
</ontology>"""
            )
            self._given_domain_contains(
                """
<domain name="TestDddDomain">
  <goal type="perform" action="top">
    <plan>
      <forget_all/>
      <findout type="goal"/>
    </plan>
  </goal>
  <goal type="resolve" question_type="wh_question" predicate="phone_number_of_contact">
    <plan>
      <findout type="wh_question" predicate="selected_contact"/>
    </plan>
  </goal>
  <goal type="perform" action="buy">
    <plan>
      <findout type="wh_question" predicate="selected_amount"/>
      <invoke_service_action name="Buy" postconfirm="true"/>
    </plan>
  </goal>
</domain>"""
            )
            self._given_grammar_contains(
                """
<grammar>
  <question speaker="user" predicate="phone_number_of_contact">
    <one-of>
      <item>tell me a phone number</item>
      <item>what is <slot type="individual" sort="contact"/>'s number</item>
      <item>tell me <slot type="individual" predicate="selected_contact"/>'s number</item>
    </one-of>
  </question>
  <individual name="contact_john">John</individual>
  <action name="buy">
    <one-of>
      <item>
        <vp>
          <infinitive>buy</infinitive>
          <imperative>buy</imperative>
          <ing-form>buying</ing-form>
          <object>apples</object>
        </vp>
      </item>
      <item>buy apples</item>
      <item>buy <slot type="individual" sort="integer"/> apples</item>
      <item>buy <slot type="individual" predicate="selected_amount"/> apples</item>
    </one-of>
  </action>
</grammar>"""
            )
        with self._given_changed_directory_to_target_dir():
            self._given_ddd_verifies_successfully()
            self._when_running_command("tala generate rasa test_ddd eng")
        self._then_stdout_contains(
            '''## intent:test_ddd:action::buy
- buy apples
- buy 0 apples
- buy 99 apples
- buy 1224 apples
- buy a hundred and fifty seven apples
- buy three apples
- buy two thousand fifteen apples

## intent:test_ddd:question::phone_number_of_contact
- tell me a phone number
- what is [John](test_ddd.sort.contact)'s number
- tell me [John]{"entity": "test_ddd.sort.contact", "role": "test_ddd.predicate.selected_contact"}'s number

## intent:test_ddd:answer
- 0
- 99
- 1224
- a hundred and fifty seven
- three
- two thousand fifteen
- [John](test_ddd.sort.contact)

## intent:test_ddd:answer_negation
- not 0
- not 99
- not 1224
- not a hundred and fifty seven
- not three
- not two thousand fifteen
- not [John](test_ddd.sort.contact)

## intent:NEGATIVE
- aboard
- about
''')  # yapf: disable  # noqa: W293
