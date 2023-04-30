// Vendors
// Assets
import { ChevronUpIcon } from "~/assets";
// Components
import {
  AccordionButton,
  AccordionHeader,
  AccordionItem,
  AccordionPanel,
  HeadlessSelectOptionProperties,
} from "solid-headless";
import AdvancedOptions from "~/components/AdvancedOptions";
import { FormOptions } from "~/components/FormOptions";

type TOptionTag = {
  title: string;
  content: any;
};

const OptionTags: TOptionTag[] = [
  { title: "Show more advanced options...", content: <AdvancedOptions /> },
];

const renderOptionButton = (
  { isSelected }: HeadlessSelectOptionProperties,
  option: TOptionTag
) => (
  <>
    <span>{option.title}</span>

    <div>
      <ChevronUpIcon
        class={`flex-0 ${
          isSelected() ? "transform rotate-180" : ""
        } w-5 h-5 text-purple-500`}
      />
    </div>
  </>
);

const renderOption = (option: TOptionTag) => (
  <AccordionItem value={option}>
    <AccordionHeader>
      <AccordionButton
        as="div"
        class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-purple-900 bg-purple-100 rounded-lg hover:bg-purple-200 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75"
      >
        {(props) => renderOptionButton(props, option)}
      </AccordionButton>
    </AccordionHeader>

    <AccordionPanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
      {option.content}
    </AccordionPanel>
  </AccordionItem>
);

export default function Home() {
  /* TODO: tab between progress bar and the actual form, some sort of logger? maybe inside the progress section */

  return (
    <form class="form" classList={{ "flex flex-col": true }}>
      <label>
        TODO: load preset
        <input type="file" name="" id="" />
      </label>
      {/* <fieldset class="first__row">
        <div class="input__container">
          <label for="websiteUrl">Website URL: </label>
          <input type="text" name="" id="websiteUrl" />
        </div>

        <div class="input__container">
          <label for="websiteUrl">Preset: </label>
          <input type="text" name="" id="websiteUrl" />
        </div>
      </fieldset>

      <Accordion class="space-y-2 mt-5" defaultValue={""} toggleable>
        <For each={OptionTags}>{renderOption}</For>
      </Accordion> */}

      <FormOptions slug="required" />
      <FormOptions slug="advanced" />

      <input
        type="submit"
        class="rounded bg-cyan-300 px-3 py-2 uppercase font-bold shadow-xl hover:shadow-md cursor-pointer"
        value={"Scrape"}
      />
    </form>
  );
}
