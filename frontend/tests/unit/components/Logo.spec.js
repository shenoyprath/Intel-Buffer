import { shallowMount } from '@vue/test-utils'
import { expect } from 'chai'

import Logo from '@/components/Logo'

describe('Logo.vue', () => {
  const wrapper = shallowMount(Logo)

  it('root element is an svg', () => {
    expect(wrapper.is('svg')).to.equal(true)
  })
})
