import { mount } from "@vue/test-utils"
import { expect } from "chai"

import BaseForm from "@/components/BaseForm"

describe("BaseForm.vue", () => {
  const wrapper = mount(BaseForm, {
    propsData: {
      action: "/random-initializer",
      method: "POST"
    }
  })

  it("checks if action starts with '/'", () => {
    const validator = wrapper
      .vm
      .$options
      .props
      .action
      .validator
    expect(validator("random")).to.not.be.ok
    expect(validator("/random")).to.be.ok
  })

  it("checks if method is a valid REST API method", () => {
    const validator = wrapper
      .vm
      .$options
      .props
      .method
      .validator
    for (const method of ["POST", "PUT", "GET", "DELETE", "PATCH"]) {
      expect(validator(method)).to.be.ok
    }
    expect(validator("random_method")).to.not.be.ok
  })
})
