import { For } from "solid-js";
import { FORM_OPTIONS } from "~/constants/form-options.constant";
import { FormSectionConfiguration } from "~/types/form.type";
import { FormSection } from "./FormSection";

type FormOption = (typeof FORM_OPTIONS)[keyof typeof FORM_OPTIONS]["inputs"][0];

function renderFormOption(formOption: FormOption) {
  return (
    <div class="m-3">
      <label>{formOption.label ?? formOption.slug}: </label>
      <input required />
    </div>
  );
}

export type FormOptionsProps = Pick<FormSectionConfiguration, "slug">;

export function FormOptions(props: FormOptionsProps) {
  const selectedFormOptions = FORM_OPTIONS[props.slug];
  return (
    <FormSection>
      <h3 class="text-2xl w-full font-bold text-left">
        {selectedFormOptions.title}
      </h3>

      <For each={selectedFormOptions.inputs}>{renderFormOption}</For>
    </FormSection>
  );
}
