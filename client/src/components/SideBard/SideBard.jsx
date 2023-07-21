import './sideBard.scss'

const SideBard = () => {

    return (
        <div className="sidebard">
            <section className="sidebard__outer-container">
                <div className="sidebard__inner-container">
                    <section className='sidebard__heading'>
                        <h1>Let's get acquainted with <span className='sidebard__text--white'>Bard</span>
                        </h1>
                    </section>
                    <section className='sidebard__age-range'>
                        <h3 className='sidebard__subheading'>What is your age range?</h3>
                        <section className='sidebard__age-range-buttons'>
                            <div className='sidebard__age-range-button'>18 - 20</div>
                            <div className='sidebard__age-range-button'>21 - 25</div>
                            <div className='sidebard__age-range-button'>26 - 30</div>
                            <div className='sidebard__age-range-button'>31 - 35</div>
                            <div className='sidebard__age-range-button'>36 - 40</div>
                            <div className='sidebard__age-range-button'>41 - 45</div>
                            <div className='sidebard__age-range-button sidebard__age-range-button--active'>46 - 50</div>
                            <div className='sidebard__age-range-button'>51+</div>
                        </section>
                    </section>
                    <section className='sidebard__know-ai'>
                        <h3 className='sidebard__subheading'>How well do you know AI?</h3>
                        <label>
                            <input
                                type='radio'
                                name='AI-knowledge'
                                value='pro'
                                className='sidebard__know-ai-radio-button' />
                            <div className='sidebard__know-ai-radio-button__circle'></div>
                            I'm a pro!
                        </label>
                        <label>
                            <input
                                type='radio'
                                name='AI-knowledge'
                                value='comfortable'
                                className='sidebard__know-ai-radio-button' />
                            <div className='sidebard__know-ai-radio-button__circle'></div>
                            I feel comfortable using AI
                        </label>
                        <label>
                            <input
                                type='radio'
                                name='AI-knowledge'
                                value='know-enough'
                                className='sidebard__know-ai-radio-button' />
                            <div className='sidebard__know-ai-radio-button__circle'></div>
                            I know enough to get by
                        </label>
                        <label>
                            <input
                                type='radio'
                                name='AI-knowledge'
                                value='minimal'
                                className='sidebard__know-ai-radio-button' />
                            <div className='sidebard__know-ai-radio-button__circle'></div>
                            I know very minimal about AI
                        </label>
                    </section>
                    <section className='sidebard__continue-button'>
                        <button>Continue</button>
                    </section>
                </div>
            </section>
        </div>
    )
}

export default SideBard