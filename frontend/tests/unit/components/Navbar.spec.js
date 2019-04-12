import { shallowMount, RouterLinkStub } from "@vue/test-utils"
import { expect } from "chai"

import BaseLogo from "@/components/BaseLogo"
import Navbar from "@/components/Navbar"

describe("Navbar.vue", () => {
  const wrapper = shallowMount(Navbar, {
    stubs: {
      RouterLink: RouterLinkStub
    }
  })

  it("root element is a nav", () => {
    expect(wrapper.is("nav")).to.be.true
  })

  it("nav header is visible", () => {
    expect(wrapper.find("div.nav-header").isVisible()).to.be.true
  })

  it("contains the logo", () => {
    expect(wrapper.contains(BaseLogo)).to.be.true
  })

  const navMenu = wrapper.find("div.nav-menu")

  it("nav menu is hidden initially", () => {
    expect(navMenu.isVisible()).to.be.false
  })

  it("nav menu is shown when hamburger button is clicked", () => {
    const hamburgerButton = wrapper.find("button.hamburger")
    hamburgerButton.trigger("click")

    expect(navMenu.isVisible()).to.be.true
  })
})
