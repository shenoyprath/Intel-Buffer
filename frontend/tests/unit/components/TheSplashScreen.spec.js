import { shallowMount } from "@vue/test-utils"
import { expect } from "chai"

import BaseLogo from "@/components/BaseLogo"
import TheSplashScreen from "@/components/TheSplashScreen"

describe("TheSplashScreen.vue", () => {
  const wrapper = shallowMount(TheSplashScreen)

  it("contains logo", () => {
    expect(wrapper.contains(BaseLogo)).to.be.true
  })
})
