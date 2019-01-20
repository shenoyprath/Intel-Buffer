import Logo from '@/components/Logo'
import Navbar from '@/components/Navbar'
import { shallowMount, RouterLinkStub } from '@vue/test-utils'
import { expect } from 'chai'

describe('Navbar.vue', () => {
  const wrapper = shallowMount(Navbar, {
    stubs: {
      RouterLink: RouterLinkStub
    }
  })

  it('root element is a nav', () => {
    expect(wrapper.is('nav')).to.equal(true)
  })

  it('nav header is visible', () => {
    expect(wrapper.find('div.nav-header').isVisible()).to.equal(true)
  })

  it('contains the logo', () => {
    expect(wrapper.contains(Logo)).to.equal(true)
  })
})
