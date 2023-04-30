import { JSX } from "solid-js";

export type CommonInputConfiguration = {
  slug: string;
  name?: string;
  id?: string;
  required?: boolean;
  label?: string | JSX.Element;
  detail?: string | JSX.Element;
  infoTooltip?: string | JSX.Element;
};

export type TextInputConfiguration = CommonInputConfiguration & {
  type: "text" | "url";
  value?: string;
};

export type TextAreaConfiguration = CommonInputConfiguration & {
  type: "textarea";
  rows?: number;
  cols?: number;
  whitespace?: "pre";
};

export type NumericInputConfiguration = CommonInputConfiguration & {
  type: "numeric";
  //   onchange: (selected: number) => void;
  value?: number;
};

export type SelectOptionConfiguration = {
  id: string | number;
  value: string | number;
};

export type SelectConfiguration<TOption extends SelectOptionConfiguration> =
  CommonInputConfiguration & {
    type: "select";
    options: TOption[];
    // onchange: (selected: TOption, id: TOption["id"]) => void;
    selected?: TOption["id"];
  };

export type CheckedConfiguration = CommonInputConfiguration & {
  type: "check";
  //   onchange: (status: boolean) => void;
  checked?: boolean;
};

export type InputConfiguration<TOption extends SelectOptionConfiguration> =
  | TextInputConfiguration
  | TextAreaConfiguration
  | NumericInputConfiguration
  | SelectConfiguration<TOption>
  | CheckedConfiguration;

export type GenericFormOption = SelectOptionConfiguration & {
  value: string;
};

export type FormSectionConfiguration<
  TOption extends SelectOptionConfiguration = GenericFormOption
> = {
  title: string;
  slug: "required" | "advanced";
  inputs: InputConfiguration<TOption>[];
};
