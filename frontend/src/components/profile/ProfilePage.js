import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { profileService } from '../../services/profileService';
import './ProfilePage.css';

const ProfilePage = () => {
  const { userId } = useParams();
  const { token } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editMode, setEditMode] = useState('profile'); // 'profile' or 'preferences'
  const [formData, setFormData] = useState({});
  const [saving, setSaving] = useState(false);

  const isOwnProfile = !userId || userId === 'me';

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const loadProfile = useCallback(async () => {
    try {
      setLoading(true);
      let data;
      if (isOwnProfile) {
        data = await profileService.getCurrentProfile(token);
      } else {
        data = await profileService.viewOtherProfile(userId, token);
      }
      setProfile(data);
      setFormData(data);
    } catch (err) {
      setError('Failed to load profile. Please try again.');
      console.error('Error loading profile:', err);
    } finally {
      setLoading(false);
    }
  }, [userId, token, isOwnProfile]);

  const handleEdit = () => {
    setIsEditing(true);
    setEditMode('profile');
  };

  const handleEditPreferences = () => {
    setIsEditing(true);
    setEditMode('preferences');
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData(profile);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      let updatedProfile;
      
      // Prepare data for backend - ensure arrays are properly formatted
      const dataToSend = { ...formData };
      
      if (editMode === 'profile') {
        updatedProfile = await profileService.updateProfile(dataToSend, token);
      } else {
        updatedProfile = await profileService.updatePreferences(dataToSend, token);
      }
      
      setProfile(updatedProfile);
      setFormData(updatedProfile);
      setIsEditing(false);
    } catch (err) {
      setError('Failed to save changes. Please try again.');
      console.error('Error saving profile:', err);
    } finally {
      setSaving(false);
    }
  };



  const formatCsv = (array) => {
    return array ? array.join(', ') : '';
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    // Handle array fields (interests, classes, otherColleges, majors)
    if (['interests', 'classes', 'otherColleges', 'majors'].includes(name)) {
      const arrayValue = value ? value.split(',').map(s => s.trim()).filter(s => s.length > 0) : [];
      setFormData(prev => ({
        ...prev,
        [name]: arrayValue
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
  };

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadProfile} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="profile-container">
        <div className="no-profile">
          <h2>Profile Not Found</h2>
          <p>The requested profile could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>{isOwnProfile ? 'My Profile' : `${profile.name || 'Anonymous'}'s Profile`}</h1>
        {isOwnProfile && !isEditing && (
          <div className="profile-actions">
            <button onClick={handleEdit} className="edit-button">
              Edit Profile
            </button>
            <button onClick={handleEditPreferences} className="edit-preferences-button">
              Edit Preferences
            </button>
          </div>
        )}
      </div>

      {isEditing ? (
        <div className="edit-form">
          <div className="edit-tabs">
            <button 
              className={`tab ${editMode === 'profile' ? 'active' : ''}`}
              onClick={() => setEditMode('profile')}
            >
              Profile
            </button>
            <button 
              className={`tab ${editMode === 'preferences' ? 'active' : ''}`}
              onClick={() => setEditMode('preferences')}
            >
              Preferences
            </button>
          </div>

          {editMode === 'profile' ? (
            <div className="form-section">
                              <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Enter your name"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="college">UC Campus</label>
                  <input
                    type="text"
                    id="college"
                    name="college"
                    value={formData.college || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., UCLA, UC Berkeley"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="school">School</label>
                  <input
                    type="text"
                    id="school"
                    name="school"
                    value={formData.school || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Engineering, Arts & Sciences"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="year">Graduation Year</label>
                  <input
                    type="number"
                    id="year"
                    name="year"
                    value={formData.year || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 2024, 2025"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="major">Major</label>
                  <input
                    type="text"
                    id="major"
                    name="major"
                    value={formData.major || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Computer Science, Biology"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="bio">Bio</label>
                  <textarea
                    id="bio"
                    name="bio"
                    value={formData.bio || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    rows={4}
                    placeholder="Tell us about yourself..."
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="interests">Interests (comma-separated)</label>
                  <input
                    type="text"
                    id="interests"
                    name="interests"
                    value={formatCsv(formData.interests)}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Hiking, Programming, Music"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="classes">Classes (comma-separated)</label>
                  <input
                    type="text"
                    id="classes"
                    name="classes"
                    value={formatCsv(formData.classes)}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., CS 180, Math 31A"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="location">Current Location</label>
                  <input
                    type="text"
                    id="location"
                    name="location"
                    value={formData.location || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Los Angeles, CA"
                  />
                </div>

                              <div className="form-group">
                  <label htmlFor="hometown">Hometown</label>
                  <input
                    type="text"
                    id="hometown"
                    name="hometown"
                    value={formData.hometown || ''}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., San Diego, CA"
                  />
                </div>
            </div>
          ) : (
            <div className="form-section">
              <div className="form-group">
                <label>Preferred Age Range</label>
                <div className="age-range">
                  <input
                    type="number"
                    name="minAge"
                    value={formData.minAge || ''}
                    onChange={handleInputChange}
                    placeholder="18"
                    className="form-input"
                  />
                  <input
                    type="number"
                    name="maxAge"
                    value={formData.maxAge || ''}
                    onChange={handleInputChange}
                    placeholder="25"
                    className="form-input"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="genderPref">Preferred Gender</label>
                <select
                  id="genderPref"
                  name="genderPref"
                  value={formData.genderPref || ''}
                  onChange={handleInputChange}
                  className="form-input"
                >
                  <option value="">Select preference</option>
                  <option value="Any">Any</option>
                  <option value="Women">Women</option>
                  <option value="Men">Men</option>
                  <option value="Non-binary">Non-binary</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="otherColleges">Other UC Campuses to See</label>
                <input
                  type="text"
                  id="otherColleges"
                  name="otherColleges"
                  value={formatCsv(formData.otherColleges)}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="e.g., UC San Diego, UC Davis"
                />
              </div>

              <div className="form-group">
                <label htmlFor="majors">Preferred Majors</label>
                <input
                  type="text"
                  id="majors"
                  name="majors"
                  value={formatCsv(formData.majors)}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="e.g., CS, Biology, Economics"
                />
              </div>
            </div>
          )}

          <div className="form-actions">
            <button onClick={handleCancel} className="cancel-button">
              Cancel
            </button>
            <button onClick={handleSave} disabled={saving} className="save-button">
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      ) : (
        <div className="profile-content">
          <div className="profile-images">
            {profile.images && profile.images.length > 0 ? (
              <div className="image-gallery">
                {profile.images.map((image, index) => (
                  <div key={index} className={`image-item ${image.isPrimary ? 'primary' : ''}`}>
                    <img src={image.imageUrl} alt={`${profile.name} ${index + 1}`} />
                    {image.isPrimary && <span className="primary-badge">Primary</span>}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-images">
                <div className="image-placeholder">
                  <span>{profile.name?.charAt(0) || 'U'}</span>
                </div>
                <p>No images uploaded</p>
              </div>
            )}
          </div>

          <div className="profile-details">
            <div className="profile-section">
              <h2>Basic Information</h2>
              <div className="info-grid">
                <div className="info-item">
                  <label>Name</label>
                  <span>{profile.name || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>Age</label>
                  <span>{profile.age || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>College</label>
                  <span>{profile.college || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>School</label>
                  <span>{profile.school || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>Major</label>
                  <span>{profile.major || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>Graduation Year</label>
                  <span>{profile.year || 'Not specified'}</span>
                </div>
              </div>
            </div>

            <div className="profile-section">
              <h2>About Me</h2>
              <p className="bio">{profile.bio || 'No bio available'}</p>
            </div>

            {profile.interests && profile.interests.length > 0 && (
              <div className="profile-section">
                <h2>Interests</h2>
                <div className="interests">
                  {profile.interests.map((interest, index) => (
                    <span key={index} className="interest-tag">{interest}</span>
                  ))}
                </div>
              </div>
            )}

            {profile.classes && profile.classes.length > 0 && (
              <div className="profile-section">
                <h2>Current Classes</h2>
                <div className="classes">
                  {profile.classes.map((className, index) => (
                    <span key={index} className="class-tag">{className}</span>
                  ))}
                </div>
              </div>
            )}

            <div className="profile-section">
              <h2>Location</h2>
              <div className="info-grid">
                <div className="info-item">
                  <label>Current Location</label>
                  <span>{profile.location || 'Not specified'}</span>
                </div>
                <div className="info-item">
                  <label>Hometown</label>
                  <span>{profile.hometown || 'Not specified'}</span>
                </div>
              </div>
            </div>

            {isOwnProfile && (
              <div className="profile-section">
                <h2>Preferences</h2>
                <div className="info-grid">
                  <div className="info-item">
                    <label>Age Range</label>
                    <span>{profile.minAge || 'Not specified'} - {profile.maxAge || 'Not specified'}</span>
                  </div>
                  <div className="info-item">
                    <label>Preferred Gender</label>
                    <span>{profile.genderPref || 'Not specified'}</span>
                  </div>
                  {profile.otherColleges && profile.otherColleges.length > 0 && (
                    <div className="info-item">
                      <label>Other UC Campuses</label>
                      <span>{profile.otherColleges.join(', ')}</span>
                    </div>
                  )}
                  {profile.majors && profile.majors.length > 0 && (
                    <div className="info-item">
                      <label>Preferred Majors</label>
                      <span>{profile.majors.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfilePage; 