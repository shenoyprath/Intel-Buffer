import { mount } from "@vue/test-utils"
import { expect } from "chai"

import BaseInput from "@/components/BaseInput"

describe("BaseInput.vue", () => {
  const testLabel = "test label"
  const maxlength = 100

  const wrapper = mount(BaseInput, {
    propsData: {
      label: testLabel,
      maxlength: maxlength,
      helper: "helper text"
    }
  })

  const input = wrapper.find("input")
  const label = wrapper.find("label")

  it("has default id for input element if one isn't given", () => {
    expect(wrapper.attributes().id).to.not.equal("")
  })

  it("has label as default placeholder", () => {
    expect(wrapper.props().placeholder).to.equal(testLabel)
    expect(input.attributes().placeholder).to.equal(testLabel)
  })

  it("removes placeholder when focused", () => {
    input.trigger("focus")
    // noinspection JSUnresolvedVariable
    expect(input.element.placeholder).to.equal("")
  })

  it("invalidates blank label", () => {
    expect(
      wrapper
        .vm
        .$options
        .props
        .label
        .validator("")
    ).to.not.be.ok
  })

  it("shows label when input is focused on", () => {
    input.trigger("focus")
    expect(label.isVisible()).to.be.true
    input.trigger("blur") // clean up
  })

  it("updates text inside input when value is updated", () => {
    const testValue = "test updates text inside input when value is updated"
    wrapper.setProps({ value: testValue })
    // noinspection JSUnresolvedVariable
    expect(input.element.value).to.equal(testValue)
  })

  it("shows label when text is present in input", () => {
    wrapper.setProps({ value: "test shows label when text is present in input" })
    expect(label.isVisible()).to.be.true
  })

  it("throws validation error for non-integer & negative maxlength", () => {
    const maxlengthValidator = wrapper
      .vm
      .$options
      .props
      .maxlength
      .validator
    expect(maxlengthValidator(-2)).to.not.be.ok
    expect(maxlengthValidator(2.5)).to.not.be.ok
  })

  it("has length to maxlength ratio when maxlength is given", () => {
    input.trigger("focus")

    const maxlengthDisplay = wrapper.find(".maxlength")
    const testValue = "test has length to maxlength ratio when maxlength is given"
    input.setValue(testValue)
    expect(maxlengthDisplay.text()).to.equal(`${testValue.length}/${maxlength}`)

    // clean up
    input.setValue("")
    input.trigger("blur")
  })

  it("shows helper text on focus", () => {
    input.trigger("focus")

    const helperText = "helper text"
    wrapper.setProps({ helper: helperText })

    const helper = wrapper.find("span.helper")
    expect(helper.text()).to.equal(helperText)
    expect(helper.isVisible()).to.be.true

    input.trigger("blur")
  })

  it("displays error when there is one and removes helper from DOM", () => {
    const testError = "test displays error when there is one and removes helper from DOM"
    wrapper.setProps({ error: testError })

    const errorDisplay = wrapper.find("span.error")
    expect(errorDisplay.text()).to.equal(testError)
    expect(errorDisplay.isVisible()).to.be.true
    expect(() => wrapper.find("span.helper").text()).to.throw()
  })

  it("changes width based on size given", () => {
    const width = 20
    wrapper.setProps({ size: width })
    expect(wrapper.element.style.width).to.equal(`${width}em`)
  })

  it("emits the value of the input when the value changes", () => {
    const testValue = "test emits the value of the input when the value changes"
    input.setValue(testValue)
    const emittedValues = wrapper.emitted().input
    expect(
      emittedValues
        .filter(value => value.includes(testValue))
        .length
    ).to.equal(1)
  })
})
