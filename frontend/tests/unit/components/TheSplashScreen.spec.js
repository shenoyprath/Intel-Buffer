import { shallowMount } from '@vue/test-utils'
import { expect } from 'chai'

import Logo from '@/components/Logo'
import TheSplashScreen from '@/components/TheSplashScreen'

describe('TheSplashScreen.vue', () => {
  const wrapper = shallowMount(TheSplashScreen)

  it('contains logo', () => {
    expect(wrapper.contains(Logo)).to.equal(true)
  })
})
