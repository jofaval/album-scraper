// Vendors
import { For } from "solid-js";
// Assets
import { ChevronUpIcon } from "~/assets";
// Components
import {
  Accordion,
  AccordionButton,
  AccordionHeader,
  AccordionItem,
  AccordionPanel,
  HeadlessSelectOptionProperties,
} from "solid-headless";
import AdvancedOptions from "~/components/AdvancedOptions";

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
  return (
    <main class="text-center mx-auto text-gray-700 p-4 container">
      <h1 class="max-6-xs text-6xl text-sky-700 font-thin uppercase my-16">
        Album scraper
      </h1>

      <form class="form">
        <fieldset class="first__row">
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
        </Accordion>

        <input type="submit" class="" value={"Scrape"} />
      </form>
    </main>
  );
}
