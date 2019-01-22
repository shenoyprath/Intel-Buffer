import Logo from '@/components/Logo'
import SplashScreen from '@/components/SplashScreen'

import { shallowMount } from '@vue/test-utils'
import { expect } from 'chai'

describe('SplashScreen.vue', () => {
  const wrapper = shallowMount(SplashScreen)

  it('contains logo', () => {
    expect(wrapper.contains(Logo)).to.equal(true)
  })
})
