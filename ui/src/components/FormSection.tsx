import { JSX } from "solid-js";

export type FormSectionProps = {
  children: JSX.Element;
};

export function FormSection(props: FormSectionProps) {
  return (
    <fieldset class="rounded flex flex-wrap items-center justify-center shadow-sm mb-5 p-5 bg-slate-50">
      {props.children}
    </fieldset>
  );
}
